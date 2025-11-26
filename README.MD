# Videoflix Backend

This is the backend of the Videoflix project, built with **Django** and **Django REST Framework**. 
Videoflix is a video streaming platform that allows users to browse and watch videos. The project focuses on implementing a secure authentication system and processing video conversions in the background. The backend handles user authentication, video streaming, and background tasks

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Build and Run the Application](#-build-and-run-the-application)
- [Running Tests](#running-tests)

---

## Requirements

- Git
- Docker Desktop with Docker Compose

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/VeyselDev/Videoflix_Backend.git
cd Videoflix_Backend
```

### 2. Environment Variables
Create a ```.env``` file in the root directory and add the following:
```
# Django Superuser
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=adminpassword
DJANGO_SUPERUSER_EMAIL=admin@example.com

# Django Settings
SECRET_KEY='<your_secret_key>'
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
CORS_ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
CORS_ALLOW_CREDENTIALS=True

# Database
DB_NAME=<your_database_name>
DB_USER=<your_database_user>
DB_PASSWORD=<your_database_password>
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_LOCATION=redis://redis:6379/1
REDIS_PORT=6379
REDIS_DB=0

# Email
EMAIL_HOST=<your_email_host>
EMAIL_PORT=<your_email_port>
EMAIL_HOST_USER=<your_email_host_user>
EMAIL_HOST_PASSWORD=<your_email_host_password>
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=<your_default_from_email>

# Cookies
COOKIE_SECURE=False
```

---

## Build and Run the Application
Make sure Docker Desktop is running and Docker Compose is available.

Run the following command ```docker-compose up --build``` to build and start all services.

The backend will be available at ```http://127.0.0.1:8000/```.

---

## Running Tests
To run all tests with pytest:
```bash
pytest
```

For code coverage:
```bash
pytest --cov=.
```

HTML report will be generated in ```htmlcov/```.