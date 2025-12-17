# Colors
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
RED	   := $(shell tput -Txterm setaf 1)
RESET  := $(shell tput -Txterm sgr0)

# Environment
DEFAULT_ENV := dev
VALID_ENVS := dev prod

BACKEND_SERVICE := backend
DB_SERVICE := postgres
REDIS_SERVICE := redis
WORKER_SERVICE := rq_worker

# Read ENV from .env
ifneq (,$(wildcard .env))
	ENV := $(shell grep '^ENV=' .env | cut -d '=' -f2)
endif

# Fallback
ENV ?= $(DEFAULT_ENV)

# Validate ENV
ifeq (,$(filter $(ENV),$(VALID_ENVS)))
	$(error Invalid ENV '$(ENV)'. Allowed: $(VALID_ENVS))
endif

# Flags
IS_DEV := $(if $(filter $(ENV),dev),true,false)

COMPOSE_BASE := docker-compose.base.yml
COMPOSE_ENV  := docker-compose.$(ENV).yml
COMPOSE_FILES := -f $(COMPOSE_BASE) -f $(COMPOSE_ENV)
DOCKER_COMPOSE := docker compose $(COMPOSE_FILES)

guard-dev:
	@[ "$(IS_DEV)" = "true" ] || { echo "$(RED)Error: This command is only available in development mode.$(RESET)"; exit 1; }

guard-prod:
	@[ "$(IS_DEV)" = "false" ] || { echo "$(RED)Error: This command is only available in production mode.$(RESET)"; exit 1; }

############################################################
# Help
############################################################
help: ## Show all available commands
	@echo
	@echo "$(GREEN)Videoflix_Backend Makefile$(RESET)"
	@echo "$(GREEN)Current Environment: $(ENV)$(RESET)"
	@echo "$(GREEN)==========================$(RESET)"
	@echo
	@echo '${YELLOW}Available commands:${RESET}'
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  ${GREEN}%-20s${RESET} %s\n", $$1, $$2}'
	@echo
	@echo


############################################################
# Core
############################################################
.PHONY: config build build-no-cache up restart down down-volumes

config: ## Show the fully merged Docker Compose configuration
	@echo "$(GREEN)Showing Docker Compose config...$(RESET)"
	$(DOCKER_COMPOSE) config

build: ## Build all images
	@echo "$(GREEN)Building images...$(RESET)"
	$(DOCKER_COMPOSE) build
	@echo "$(GREEN)Build completed.$(RESET)"

build-no-cache: ## Build all images without cache
	@echo "$(GREEN)Building images (no cache)...$(RESET)"
	$(DOCKER_COMPOSE) build --no-cache
	@echo "$(GREEN)Build completed.$(RESET)"

up: ## Start all services in detached mode
	@echo "$(GREEN)Starting containers...$(RESET)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)Containers started.$(RESET)"

start: build up migrate ## Quick start: build, up, migrate
	@echo "$(GREEN)Application ready!$(RESET)"

restart: ## Restart all running services
	@echo "$(GREEN)Restarting containers...$(RESET)"
	$(DOCKER_COMPOSE) restart
	@echo "$(GREEN)Restart completed.$(RESET)"

restart-fresh: down build up migrate ## Complete rebuild and restart
	@echo "$(GREEN)Fresh restart completed!$(RESET)"

down: ## Stop containers and remove networks
	@echo "$(GREEN)Stopping containers...$(RESET)"
	$(DOCKER_COMPOSE) down

down-volumes: ## Stop containers and remove volumes
	@echo "$(GREEN)Stopping containers and deleting volumes...$(RESET)"
	$(DOCKER_COMPOSE) down -v


############################################################
# Deployment
############################################################
.PHONY: deploy

deploy: ## Deploy (PROD only)
	@echo "$(YELLOW)PRODUCTION DEPLOYMENT$(RESET)"
	@echo "$(YELLOW)=====================$(RESET)"
	@echo
	@echo "$(GREEN)[1/7] Fetching latest code from origin...$(RESET)"
	@git fetch origin main
	@echo "$(GREEN)[2/7] Resetting local branch to origin/main...$(RESET)"
	@git reset --hard origin/main
	@echo "$(GREEN)[3/7] Building images...$(RESET)"
	@$(MAKE) build
	@echo "$(GREEN)[4/7] Stopping old containers...$(RESET)"
	@$(MAKE) down
	@echo "$(GREEN)[5/7] Starting new containers...$(RESET)"
	@$(MAKE) up
	@echo "$(GREEN)[6/7] Running migrations...$(RESET)"
	@$(MAKE) migrate
	@echo "$(GREEN)[7/7] Collecting static files...$(RESET)"
	@$(MAKE) collectstatic
	@echo "$(GREEN) Deployment completed successfully!$(RESET)"


############################################################
# Maintenance
############################################################
.PHONY: clean

clean: ## Remove all containers, volumes, networks and unused images
	@echo "$(YELLOW)This will remove all containers, volumes, networks and unused images!$(RESET)"
	@read -p "Continue? (y/n): " confirm && [ $$confirm = "y" ]
	@echo "$(GREEN)Cleaning system...$(RESET)"
	$(DOCKER_COMPOSE) down -v --remove-orphans
	docker system prune -f
	@echo "$(GREEN)Cleanup completed.$(RESET)"


############################################################
# Logs
############################################################
.PHONY: logs logs-backend logs-worker

logs: ## Show logs for all services
	@echo "$(GREEN)Streaming logs...$(RESET)"
	$(DOCKER_COMPOSE) logs -f

logs-backend: ## Show backend logs
	$(DOCKER_COMPOSE) logs -f $(BACKEND_SERVICE)

logs-worker: ## Show worker logs
	$(DOCKER_COMPOSE) logs -f $(WORKER_SERVICE)


############################################################
# Shell Access
############################################################
.PHONY: shell-backend shell-postgres shell-redis

shell-backend: ## Open shell inside backend container
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) sh

shell-postgres: ## Open Postgres shell
	$(DOCKER_COMPOSE) exec $(DB_SERVICE) psql -U $(DB_USER) -d $(DB_NAME)

shell-redis: ## Open Redis CLI
	$(DOCKER_COMPOSE) exec $(REDIS_SERVICE) redis-cli


############################################################
# Django Management
############################################################
.PHONY: makemigrations migrate collectstatic createsuperuser

makemigrations: guard-dev ## Create new migrations (DEV only)
	@echo "$(GREEN)Creating migrations...$(RESET)"
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py makemigrations

migrate: ## Apply database migrations
	@echo "$(GREEN)Running migrations...$(RESET)"
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py migrate

collectstatic: ## Collect static files
	@echo "$(GREEN)Collecting static files...$(RESET)"
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py collectstatic --noinput

createsuperuser: ## Create superuser
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py createsuperuser


############################################################
# Database Backup & Restore
############################################################
.PHONY: db-backup db-restore db-reset

db-backup: ## Create a database backup
	@echo "$(GREEN)Creating database backup...$(RESET)"
	@TS=$$(date +%Y%m%d_%H%M%S); \
	$(DOCKER_COMPOSE) exec $(DB_SERVICE) pg_dump -U $(DB_USER) $(DB_NAME) > backup_$${TS}.sql; \
	echo "$(GREEN)Backup created: backup_$${TS}.sql$(RESET)"

db-restore: ## Restore database (usage: make db-restore FILE=backup.sql)
	@[ -f "$(FILE)" ] || { echo "$(RED)Error: File $(FILE) not found$(RESET)"; exit 1; }
	@echo "$(YELLOW)Restoring from $(FILE)...$(RESET)"
	cat $(FILE) | $(DOCKER_COMPOSE) exec -T $(DB_SERVICE) psql -U $(DB_USER) $(DB_NAME)
	@echo "$(GREEN)Restore completed.$(RESET)"

db-reset: guard-dev ## Reset database (DEV only)
	@echo "$(RED)WARNING: This will delete ALL database data.$(RESET)"
	@read -p "Continue? (y/n): " confirm && [ $$confirm = "y" ]
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py flush --noinput
	@echo "$(GREEN)Database reset completed.$(RESET)"


############################################################
# Tests
############################################################
.PHONY: test test-coverage

test: guard-dev ## Run Django tests (DEV only)
	@echo "$(GREEN)Running tests...$(RESET)"
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py test

test-coverage: guard-dev ## Run tests with coverage (DEV only)
	@echo "$(GREEN)Running tests with coverage...$(RESET)"
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) coverage run --source='.' manage.py test
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) coverage report


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
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py check --deploy

generate-secret-key: ## Generate Django SECRET_KEY
	@python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
