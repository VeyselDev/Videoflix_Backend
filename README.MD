# Videoflix Backend

This is the backend of the Videoflix project, built with **Django** and **Django REST Framework**. 
Videoflix is a video streaming platform that allows users to browse and watch videos. The project focuses on implementing a secure authentication system and processing video conversions in the background. The backend handles user authentication, video streaming, and background tasks

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Build and Run the Application](#-build-and-run-the-application)
- [Running Tests](#running-tests)
- [License](#license)

---

## Requirements

- git
- Python 3.11+  
- pip (Python package manager)  
- Virtualenv (recommended)
- Docker Desktop with docker-compose

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/VeyselDev/Videoflix_Backend.git
cd Videoflix_Backend
```

### 2. Create a virtual environment
```bash
# Linux/macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Environment Variables
Create a ```.env``` file in the root directory and add the following:
```bash
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=adminpassword
DJANGO_SUPERUSER_EMAIL=admin@example.com

SECRET_KEY="<secret_key>"
DEBUG=True
ALLOWED_HOSTS=<allowed_hosts>
CSRF_TRUSTED_ORIGINS=<csrf_trusted_origins>

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=db
DB_PORT=5432

REDIS_HOST=redis
REDIS_LOCATION=redis://redis:6379/1
REDIS_PORT=6379
REDIS_DB=0

EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email_user
EMAIL_HOST_PASSWORD=your_email_user_password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=default_from_email


COOKIE_SECURE=False
```

## Build and Run the Application
Run the following command ```docker-compose up --build``` to build and start all services:

The backend will be available at ```http://127.0.0.1:8000/```.

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

## License
This project is licensed under the MIT License.