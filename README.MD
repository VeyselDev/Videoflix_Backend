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
Open the terminal and run:

```bash
git clone https://github.com/VeyselDev/Videoflix_Backend.git
cd Videoflix_Backend
```

### 2. Environment Variables
Create a `.env` file in the root directory by copying the existing `.env.template` file.

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