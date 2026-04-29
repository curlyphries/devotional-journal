# Devotional Journal

An open-source, bilingual (English/Spanish) men's devotional Bible journal designed for web and mobile.

## Features

- **Daily Scripture Reading** - Structured reading plans with progress tracking
- **AI-Generated Reflection Prompts** - LLM-powered questions tailored to each passage
- **Private Journaling** - Encrypted at rest, your thoughts stay yours
- **Group Accountability** - Leaders see engagement metrics, never private content
- **Bilingual Support** - Native English/Spanish with code-switching support
- **Streak Tracking** - Build consistent devotional habits

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5.x + Django REST Framework |
| Frontend | React 18+ (TypeScript) |
| Database | PostgreSQL 16+ |
| Cache/Broker | Redis |
| Task Queue | Celery |
| LLM | Ollama (dev) / OpenAI/Anthropic (prod) |

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Node.js 20+

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/devotional-journal.git
cd devotional-journal

# Start services with Docker Compose
docker compose up -d

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements/dev.txt
python manage.py migrate
python manage.py runserver

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Database
DATABASE_URL=postgres://user:pass@localhost:5432/devotional

# Redis
REDIS_URL=redis://localhost:6379/0

# Encryption
ENCRYPTION_ROOT_KEY=your-32-byte-key-here

# LLM (development)
LLM_BACKEND=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# Email (magic link auth)
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
```

## Project Structure

```
devotional-journal/
├── backend/          # Django API
├── frontend/         # React web app
├── shared/           # Shared TypeScript utilities
├── mobile/           # React Native app (Phase 4)
├── scripts/          # Data loading scripts
├── docs/             # Documentation
└── docker-compose.yml
```

## Documentation

- [API Documentation](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Encryption & Security](docs/ENCRYPTION.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the AGPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built for men seeking consistent devotional habits and church leaders who need engagement tools for men's groups.
