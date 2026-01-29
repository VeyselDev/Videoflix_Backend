# Detect if running on Windows
ifeq ($(OS),Windows_NT)
	IS_WINDOWS := true
	CONFIRM_CMD := powershell -Command "$$val = Read-Host 'Continue? (y/n)'; if ($$val -ne 'y') { exit 1 }"
else
	IS_WINDOWS := false
	CONFIRM_CMD := printf "Continue? (y/n): " && read confirm && [ "$$confirm" = "y" ]
endif

# Colors (Windows: empty, Linux/macOS: tput)
GREEN  := $(if $(IS_WINDOWS),,$(shell tput setaf 2))
YELLOW := $(if $(IS_WINDOWS),,$(shell tput setaf 3))
RED    := $(if $(IS_WINDOWS),,$(shell tput setaf 1))
RESET  := $(if $(IS_WINDOWS),,$(shell tput sgr0))

# Environment settings: default and allowed values
DEFAULT_ENV := dev
VALID_ENVS := dev prod

# Docker service names used in this project
BACKEND_SERVICE := backend
DB_SERVICE := postgres
REDIS_SERVICE := redis
WORKER_SERVICE := rq_worker
SCHEDULER_SERVICE := rq_scheduler

# Load environment variables from .env if the file exists
ifneq (,$(wildcard .env))
	include .env
	export
endif

# Use DEFAULT_ENV if ENV is not already set
ENV ?= $(DEFAULT_ENV)

# Validate that ENV is one of the allowed environments
ifeq (,$(filter $(ENV),$(VALID_ENVS)))
	$(error Invalid ENV '$(ENV)'. Allowed: $(VALID_ENVS))
endif

# Flag indicating if the current environment is development
IS_DEV := $(if $(filter $(ENV),dev),true,false)

# Compose files configuration and docker-compose command
COMPOSE_BASE := docker-compose.base.yml
COMPOSE_ENV  := docker-compose.$(ENV).yml
COMPOSE_FILES := -f $(COMPOSE_BASE) -f $(COMPOSE_ENV)
DOCKER_COMPOSE := docker compose $(COMPOSE_FILES)

# Guard to ensure a target runs only in development environment
guard-dev:
ifneq ($(IS_DEV),true)
	$(error $(RED)Error: This command is only available in development mode (ENV=dev)$(RESET))
endif

# Guard to ensure a target runs only in production environment
guard-prod:
ifeq ($(IS_DEV),true)
	$(error $(RED)Error: This command is only available in production mode (ENV=prod)$(RESET))
endif

############################################################
# Help
############################################################
.PHONY: help

help:
	$(info )
	$(info Videoflix_Backend Makefile)
	$(info Current Environment: $(ENV))
	$(info ==========================)
	$(info )
	$(info Available commands:)
ifeq ($(IS_WINDOWS),true)
	@powershell -NoProfile -ExecutionPolicy Bypass -Command \
		"Get-Content Makefile | ForEach-Object { \
			if ($$_.ToString() -match '^(?<cmd>[a-zA-Z0-9_-]+):.*?## (?<desc>.*)') { \
				'  {0,-22} {1}' -f $$Matches['cmd'], $$Matches['desc'] \
			} \
		} | Sort-Object"
else
	@grep -Eh '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  ${GREEN}%-20s${RESET} %s\n", $$1, $$2}'
endif


############################################################
# Core
############################################################
.PHONY: config build build-no-cache up start start-quick restart restart-fresh down down-volumes

config: ## Show the fully merged Docker Compose configuration
	@echo "$(GREEN)Showing Docker Compose config...$(RESET)"
	$(DOCKER_COMPOSE) config

build: ## Build all images
	@echo "$(GREEN)Building images...$(RESET)"
	$(DOCKER_COMPOSE) build
	@echo "$(GREEN)Build completed.$(RESET)"

build-no-cache: ## Build all images without cache
	@echo "$(GREEN)Building images without cache...$(RESET)"
	$(DOCKER_COMPOSE) build --no-cache
	@echo "$(GREEN)Build completed.$(RESET)"

up: ## Start all services in detached mode
	@echo "$(GREEN)Starting containers...$(RESET)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)Containers started.$(RESET)"

start: build-no-cache up migrate ## Build images without cache, start services and run migrations
	@echo "$(GREEN)Application ready!$(RESET)"

start-quick: build up migrate ## Incremental start: build if needed, start services and run migrations
	@echo "$(GREEN)Application ready!$(RESET)"

restart: ## Restart running containers without rebuilding images
	@echo "$(GREEN)Restarting containers...$(RESET)"
	$(DOCKER_COMPOSE) restart
	@echo "$(GREEN)Restart completed.$(RESET)"

restart-fresh: down build up migrate ## Stop and delete containers, rebuild images, start services and run migrations
	@echo "$(GREEN)Fresh restart completed!$(RESET)"

down: ## Stop and delete containers and networks
	@echo "$(GREEN)Stopping and deleting containers and networks...$(RESET)"
	$(DOCKER_COMPOSE) down

down-volumes: ## Stop and delete containers, networks and volumes
	@echo "$(GREEN)Stopping and deleting containers, networks and volumes...$(RESET)"
	$(DOCKER_COMPOSE) down -v


############################################################
# Deployment
############################################################
.PHONY: deploy

deploy: guard-prod ## Deploy (PROD only)
	@echo "$(YELLOW)PRODUCTION DEPLOYMENT$(RESET)"
	@echo "$(YELLOW)=====================$(RESET)"
	@echo
	@echo "$(GREEN)[1/8] Running Django security checks...$(RESET)"
	@$(MAKE) check-security
	@echo "$(GREEN)[2/8] Fetching latest code from origin...$(RESET)"
	@git fetch origin main
	@echo "$(GREEN)[3/8] Resetting local branch to origin/main...$(RESET)"
	@git reset --hard origin/main
	@echo "$(GREEN)[4/8] Building images...$(RESET)"
	@$(MAKE) build
	@echo "$(GREEN)[5/8] Stopping old containers...$(RESET)"
	@$(MAKE) down
	@echo "$(GREEN)[6/8] Starting new containers...$(RESET)"
	@$(MAKE) up
	@echo "$(GREEN)[7/8] Running migrations...$(RESET)"
	@$(MAKE) migrate
	@echo "$(GREEN)[8/8] Collecting static files...$(RESET)"
	@$(MAKE) collectstatic
	@echo "$(GREEN) Deployment completed successfully!$(RESET)"


############################################################
# Maintenance
############################################################
.PHONY: clean

clean: ## Remove all containers, volumes, networks and unused images
	@echo "$(YELLOW)This will remove all containers, volumes, networks and unused images!$(RESET)"
	@$(CONFIRM_CMD)
	@echo "$(GREEN)Cleaning system...$(RESET)"
	$(DOCKER_COMPOSE) down -v --remove-orphans
	docker system prune -f
	@echo "$(GREEN)Cleanup completed.$(RESET)"


############################################################
# Logs
############################################################
.PHONY: logs logs-postgres logs-redis logs-backend logs-worker logs-scheduler

logs: ## Show logs for all services
	@echo "$(GREEN)Streaming logs...$(RESET)"
	$(DOCKER_COMPOSE) logs -f

logs-postgres: ## Show Postgres logs
	@echo "$(GREEN)Streaming Postgres logs...$(RESET)"
	$(DOCKER_COMPOSE) logs -f $(DB_SERVICE)

logs-redis: ## Show Redis logs
	@echo "$(GREEN)Streaming Redis logs...$(RESET)"
	$(DOCKER_COMPOSE) logs -f $(REDIS_SERVICE)

logs-backend: ## Show backend logs
	$(DOCKER_COMPOSE) logs -f $(BACKEND_SERVICE)

logs-worker: ## Show worker logs
	$(DOCKER_COMPOSE) logs -f $(WORKER_SERVICE)

logs-scheduler: ## Show scheduler logs
	$(DOCKER_COMPOSE) logs -f $(SCHEDULER_SERVICE)


############################################################
# Shell Access
############################################################
.PHONY: shell-postgres shell-redis shell-backend shell-django

shell-postgres: ## Open Postgres shell
	$(DOCKER_COMPOSE) exec $(DB_SERVICE) psql -U $(DB_USER) -d $(DB_NAME)

shell-redis: ## Open Redis CLI
	$(DOCKER_COMPOSE) exec $(REDIS_SERVICE) redis-cli

shell-backend: ## Open regular shell inside backend container
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) sh

shell-django: ## Open Django shell inside backend container
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py shell


############################################################
# Django Management
############################################################
.PHONY: makemigrations migrate collectstatic createsuperuser

makemigrations: guard-dev ## Create new migrations (DEV only)
	@echo "$(GREEN)Creating migrations...$(RESET)"
	$(DOCKER_COMPOSE) run --rm $(BACKEND_SERVICE) python manage.py makemigrations

migrate: ## Apply database migrations
	@echo "$(GREEN)Running migrations...$(RESET)"
	$(DOCKER_COMPOSE) run --rm $(BACKEND_SERVICE) python manage.py migrate

collectstatic: guard-prod ## Collect static files (PROD only)
	@echo "$(GREEN)Collecting static files...$(RESET)"
	$(DOCKER_COMPOSE) run --rm $(BACKEND_SERVICE) python manage.py collectstatic --noinput

createsuperuser: ## Create superuser
	$(DOCKER_COMPOSE) run --rm $(BACKEND_SERVICE) python manage.py createsuperuser


############################################################
# Database
############################################################
.PHONY: db-reset

db-reset: guard-dev ## Reset database (DEV only)
	@echo "$(RED)WARNING: This will delete ALL database data.$(RESET)"
	@$(CONFIRM_CMD)
	$(DOCKER_COMPOSE) run --rm $(BACKEND_SERVICE) python manage.py flush --noinput
	@echo "$(GREEN)Database reset completed.$(RESET)"


############################################################
# Tests
############################################################
.PHONY: pytest pytest-html-report

pytest: guard-dev ## Run Django pytests with coverage (DEV only)
	@echo "$(GREEN)Running pytests with coverage...$(RESET)"
	$(DOCKER_COMPOSE) run --rm $(BACKEND_SERVICE) pytest

pytest-html-report: guard-dev ## Run Django pytests with coverage + HTML report (DEV only)
	@echo "$(GREEN)Running pytests with coverage and HTML report...$(RESET)"
	$(DOCKER_COMPOSE) run --rm $(BACKEND_SERVICE) pytest --cov-report=html


############################################################
# Seeders
############################################################
.PHONY: seed-videos

seed-videos: ## Seed sample videos
	@echo "$(GREEN)Seeding sample videos...$(RESET)"
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py seed_videos


############################################################
# Monitoring
############################################################
.PHONY: ps ps-detailed

ps: ## Show running containers
	$(DOCKER_COMPOSE) ps

ps-detailed: ## Show all containers (including stopped)
	$(DOCKER_COMPOSE) ps -a


############################################################
# Misc
############################################################
.PHONY: check-security generate-secret-key

check-security: ## Run Django security checks
	$(DOCKER_COMPOSE) run --rm $(BACKEND_SERVICE) python manage.py check --deploy

generate-secret-key: ## Generate Django SECRET_KEY
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(f'Secret Key: {get_random_secret_key()}')"