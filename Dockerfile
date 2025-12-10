# ============================================
# Base Stage - Common dependencies
# ============================================
FROM python:3.12-alpine AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apk add --no-cache \
    bash \
    build-base \
    curl \
    ffmpeg \
    jpeg-dev \
    libffi-dev \
    musl-dev \
    postgresql-client \
    postgresql-dev \
    redis \
    zlib-dev \
    && rm -rf /var/cache/apk/*

# ============================================
# Dependencies Stage - Install Python packages
# ============================================
FROM base AS dependencies

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .
RUN rm -rf .git .env* .gitignore *.template docker-compose* Makefile

# ============================================
# Development Stage
# ============================================
FROM dependencies AS dev
COPY . .
RUN rm -rf .git .env* .gitignore *.template docker-compose* Makefile

COPY entrypoint.backend.sh .
RUN chmod +x entrypoint.backend.sh

RUN mkdir -p /app/media /app/static && \
    chmod -R 755 /app

EXPOSE 8000

ENTRYPOINT ["./entrypoint.backend.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ============================================
# Production Stage
# ============================================
FROM dependencies AS prod

COPY . .
RUN rm -rf .git .env* .gitignore *.template docker-compose* Makefile

COPY entrypoint.backend.sh .
RUN chmod +x entrypoint.backend.sh

RUN addgroup -g 1000 deployer && \
    adduser -D -u 1000 -G deployer deployer

RUN mkdir -p /app/media /app/static && \
    chown -R deployer:deployer /app/media /app/static && \
    chmod -R 775 /app/media && \
    chmod -R 755 /app/static

USER deployer

EXPOSE 8000

ENTRYPOINT ["./entrypoint.backend.sh"]

CMD gunicorn core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-5} \
    --threads ${GUNICORN_THREADS:-2} \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --max-requests ${GUNICORN_MAX_REQUESTS:-1000} \
    --max-requests-jitter ${GUNICORN_MAX_REQUESTS_JITTER:-50} \
    --access-logfile - \
    --error-logfile - \
    --log-level info