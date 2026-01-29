# Videoflix Backend
Videoflix is a video streaming platform where users can browse and watch videos. 
The backend, built with **Django** and **Django REST Framework**, manages user authentication, video streaming and background processing of video conversions.

---

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Commands Overview](#quick-commands-overview)
- [Build and Run the Application](#build-and-run-the-application)
- [Tests](#tests)

---

## Requirements
- Git
- Docker Desktop with Docker Compose
- Make

---

## Installation
### 1. Clone the repository
Open the terminal and run:

```bash
git clone https://github.com/VeyselDev/Videoflix_Backend.git
cd Videoflix_Backend
```

### 2. Environment Variables
The project uses separate environment configurations for development and production.

#### 2.1 Create the `.env` file
Copy the appropriate template depending on your environment:

**macOS / Linux:**
```bash
# For development
cp .env.dev.template .env
```

```bash
# For production
cp .env.prod.template .env
```

**Windows:**
```bash
# For development
copy .env.dev.template .env
```

```bash
# For production
copy .env.prod.template .env
```

#### 2.2 Update the configuration
Open the `.env` file and set your own values.

---

## Quick Commands Overview
Running this command displays a list of all available Makefile commands along with a short description for each. This is useful to quickly see what actions you can perform.
```bash
make help
```

---

## Build and Run the Application
Make sure **Docker Desktop** is running and **Docker Compose** is available.

Run the following command to build and start all services:
```bash
make up
```

The backend will be available at:
```
http://127.0.0.1:8000/
```

---

## Seed Videos
Populates the database with sample videos defined in `seed_data/videos.json`.

Run the following command to seed the initial video data:

```bash
make seed-videos
```

---

## Tests
This project uses **pytest** for unit tests and **pytest-cov** for measuring code coverage.

### 1. Running Tests
Run all tests with coverage displayed in the terminal:

```bash
make pytest
```

### 2. Running Tests with HTML Coverage Report
Run all tests with coverage and generate an HTML report:

```bash
make pytest-html-report
```
The HTML coverage report is generated in the `htmlcov/` directory and can be opened in your browser:

```bash
# macOS
open htmlcov/index.html
```

```bash
# Linux
xdg-open htmlcov/index.html
```

```bash
# Windows
start htmlcov\index.html
```