# Development Guide

## Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose (optional)

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/curlyphries/devotional-journal.git
cd devotional-journal

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start all services
docker compose up -d

# Run migrations
docker compose exec backend python manage.py migrate

# Load seed data
docker compose exec backend python scripts/load_kjv.py
docker compose exec backend python scripts/seed_plans.py

# Access the app
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/api/v1/
# Admin: http://localhost:8000/admin/
```

### Manual Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements/dev.txt

# Copy environment file and configure
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load seed data
python scripts/load_kjv.py
python scripts/seed_plans.py

# Start development server
python manage.py runserver
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start development server
npm run dev
```

## Project Structure

```
devotional-journal/
├── backend/
│   ├── apps/
│   │   ├── users/          # User auth, profiles
│   │   ├── bible/          # Bible text provider
│   │   ├── plans/          # Reading plans
│   │   ├── journal/        # Encrypted journal entries
│   │   ├── prompts/        # LLM prompt generation
│   │   ├── streaks/        # Engagement tracking
│   │   └── groups/         # Group management (Phase 2)
│   ├── config/             # Django settings
│   ├── shared/             # Shared utilities
│   ├── scripts/            # Data loading scripts
│   └── requirements/       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── api/            # API client
│   │   ├── components/     # React components
│   │   ├── context/        # React context providers
│   │   ├── pages/          # Page components
│   │   ├── i18n/           # Translations
│   │   └── styles/         # CSS/Tailwind
│   └── public/
└── docs/                   # Documentation
```

## Running Tests

### Backend

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific app tests
pytest apps/journal/

# Run marked tests
pytest -m "not slow"
```

### Frontend

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

## Code Style

### Backend

- **Formatter:** Black
- **Linter:** Ruff
- **Type Hints:** Required for all functions

```bash
# Format code
black .

# Lint code
ruff check .

# Fix auto-fixable issues
ruff check --fix .
```

### Frontend

- **Formatter:** Prettier
- **Linter:** ESLint
- **TypeScript:** Strict mode

```bash
# Format code
npm run format

# Lint code
npm run lint

# Type check
npx tsc --noEmit
```

## Environment Variables

### Backend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Debug mode | `False` |
| `DATABASE_URL` | PostgreSQL connection | Required |
| `REDIS_URL` | Redis connection | `redis://localhost:6379/0` |
| `ENCRYPTION_ROOT_KEY` | 32-char encryption key | Required |
| `LLM_BACKEND` | `ollama` or `anthropic` | `ollama` |
| `OLLAMA_BASE_URL` | Ollama API URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Ollama model name | `llama3.1:8b` |

### Frontend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:8000/api/v1` |

## Database Migrations

```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

## Celery Tasks

```bash
# Start Celery worker
celery -A config worker -l info

# Start Celery Beat (scheduler)
celery -A config beat -l info

# Start both with flower monitoring
celery -A config flower
```

## LLM Development

For local development, use Ollama:

```bash
# Install Ollama (Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Pull the model
ollama pull llama3.1:8b

# Start Ollama server
ollama serve
```

Set in `.env`:
```
LLM_BACKEND=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

## Common Issues

### "Cannot find module" errors in frontend
Run `npm install` to install dependencies.

### Database connection errors
Ensure PostgreSQL is running and `DATABASE_URL` is correct.

### LLM prompts failing
Check Ollama is running: `curl http://localhost:11434/api/tags`

### Encryption errors
Ensure `ENCRYPTION_ROOT_KEY` is exactly 32 characters.
