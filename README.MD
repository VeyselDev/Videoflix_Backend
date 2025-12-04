# Videoflix Backend
 
Videoflix is a video streaming platform that allows users to browse and watch videos. 
The project focuses on implementing an authentication system and processing video conversions in the background. 
The backend handles user authentication, video streaming and background tasks.
It is built with **Django** and **Django REST Framework**.

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Build and Run the Application](#-build-and-run-the-application)
- [Seed initial data](#seed-initial-data)
- [Running Tests](#running-tests)

---

## Requirements

- Git
- Docker Desktop with Docker Compose

---

## Installation

### 1. Clone the repository
Open the terminal and run:

```bash
git clone https://github.com/VeyselDev/Videoflix_Backend.git
cd Videoflix_Backend
```

### 2. Environment Variables
Run the following command to create a `.env` file by copying the existing `.env.template`:

**macOS / Linux**
```bash
cp .env.template .env
```

**Windows PowerShell**
```bash
copy .env.template .env
```

After creating the file, open the `.env` file and update the values with your own configuration.

---

## Build and Run the Application
Make sure **Docker Desktop** is running and **Docker Compose** is available.

Run the following command to build and start all services:
```bash
docker-compose up --build
```

The backend will be available at:
```
http://127.0.0.1:8000/
```

---

## Seed initial data
To seed the database with initial data such as users and videos, open a new terminal while the Docker containers are already running and execute the following commands:

### 1. Seed Users
```bash
docker-compose exec web python manage.py seed_users
```

The default login credentials are `user@example.com` for the email and `password` for the password.

### 2. Seed Videos
```bash
docker-compose exec web python manage.py seed_videos
```

---

## Tests
This project uses **pytest** for unit tests and **pytest-cov** for code coverage.

### Running all tests
Open a new terminal while the Docker containers are already running and execute the following command to run all tests, display code coverage and create an HTML report:

```bash
docker-compose exec web pytest
```

The HTML report is generated in the ```htmlcov/``` directory.