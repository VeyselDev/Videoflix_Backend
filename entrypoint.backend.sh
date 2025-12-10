#!/bin/bash
set -e

# ============================================
# Configuration
# ============================================
MAX_RETRIES=30
RETRY_INTERVAL=2


# ============================================
# START
# ============================================
echo "==========================================="
echo "Starting Videoflix Backend Setup"
echo "Environment: ${ENV}"
echo "==========================================="


# ============================================
# Color codes
# ============================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'


# ============================================
# Wait for database
# ============================================
echo "Waiting for database..."
RETRY_COUNT=0

until pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" > /dev/null 2>&1; do
  RETRY_COUNT=$((RETRY_COUNT + 1))

  if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo -e "${RED} Database connection failed after ${MAX_RETRIES} attempts${NC}"
    exit 1
  fi

  echo "Database is unavailable - attempt ${RETRY_COUNT}/${MAX_RETRIES} - sleeping"
  sleep $RETRY_INTERVAL
done
echo -e "${GREEN} Database is ready${NC}"


# ============================================
# Wait for Redis
# ============================================
echo "Waiting for Redis..."
RETRY_COUNT=0

until redis-cli -h "${REDIS_HOST}" -p "${REDIS_PORT}" ping > /dev/null 2>&1; do
  RETRY_COUNT=$((RETRY_COUNT + 1))
  if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo -e "${RED} Redis connection failed after ${MAX_RETRIES} attempts${NC}"
    exit 1
  fi
  echo "Redis is unavailable - attempt ${RETRY_COUNT}/${MAX_RETRIES} - sleeping"
  sleep $RETRY_INTERVAL
done
echo -e "${GREEN} Redis is ready${NC}"


# ============================================
# Run migrations
# ============================================
echo "Running database migrations..."
if python manage.py migrate --noinput; then
  echo -e "${GREEN} Migrations completed${NC}"
else
  echo -e "${RED} Migrations failed${NC}"
  exit 1
fi


# ============================================
# Collect static files (Production)
# ============================================
if [ "${ENV}" = "prod" ]; then
  echo "Collecting static files..."
  if python manage.py collectstatic --noinput --clear; then
    echo -e "${GREEN} Static files collected${NC}"
  else
    echo -e "${YELLOW} Warning: Static files collection failed${NC}"
  fi
else
  echo -e "${YELLOW} Skipping static files collection in development mode${NC}"
fi


# ============================================
# Create or update superuser (optional)
# ============================================
if [ "${CREATE_SUPERUSER:-false}" = "true" ]; then
  echo "Superuser check..."

  python manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if not username or not password:
    print("Superuser env vars missing. Skipping.")
else:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print("Superuser created")
    else:
        u = User.objects.get(username=username)
        u.set_password(password)
        u.is_staff = True
        u.is_superuser = True
        u.save()
        print("Superuser updated")
EOF
fi

# ============================================
# Start application
# ============================================
echo "==========================================="
echo "Setup completed. Starting application..."
echo "Command: $@"
echo "==========================================="

exec "$@"
