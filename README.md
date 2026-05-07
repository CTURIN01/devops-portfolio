# DevOps Portfolio — Project 1: Containerized Django REST API with CI/CD

A production-patterned REST API built with Django and MySQL, fully containerized with Docker, and deployed with an automated CI/CD pipeline using GitHub Actions.

## 🏗️ Architecture

```
GitHub Push → GitHub Actions CI → Run Tests → Build Docker Image
                                      ↓
                              Django REST API
                                      ↓
                            MySQL (Dockerized)
```

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| API Framework | Django 5.1.5 + Django REST Framework |
| Database | MySQL 8.0 |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Language | Python 3.11 |

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Python 3.11+

### Run Locally

```bash
# Clone the repo
git clone https://github.com/CTURINO01/devops-portfolio.git
cd devops-portfolio/backend

# Copy environment variables
cp .env.example .env

# Start all services
docker-compose up --build

# API is live at:
http://localhost:8000/api/
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/projects/` | List all projects |
| POST | `/api/projects/` | Create a project |
| GET | `/api/projects/<id>/` | Get a project |
| PUT | `/api/projects/<id>/` | Update a project |
| DELETE | `/api/projects/<id>/` | Delete a project |

## ⚙️ CI/CD Pipeline

Every push to `main` automatically:

1. Spins up a MySQL 8.0 service container
2. Installs Python dependencies
3. Runs Django migrations
4. Runs the test suite
5. Builds the Docker image

## 📁 Project Structure

```
devops-portfolio/
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions pipeline
├── backend/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── manage.py
│   ├── core/               # Django settings
│   └── api/                # REST API app
└── README.md
```

## 🔑 Environment Variables

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=devops_db
DB_USER=devops_user
DB_PASSWORD=yourpassword
DB_HOST=db
DB_PORT=3306
```