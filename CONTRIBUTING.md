# Contributing to Devotional Journal

Thank you for your interest in contributing to Devotional Journal!

## Code of Conduct

Be respectful, inclusive, and constructive. This project serves a faith-based community.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up the development environment (see README.md)
4. Create a feature branch: `git checkout -b feature/your-feature-name`

## Development Workflow

### Backend (Django)

```bash
cd backend
source venv/bin/activate
pip install -r requirements/dev.txt

# Run tests
pytest

# Run linting
ruff check .
black --check .

# Format code
black .
ruff check --fix .
```

### Frontend (React)

```bash
cd frontend
npm install

# Run tests
npm test

# Run linting
npm run lint

# Format code
npm run format
```

## Pull Request Process

1. **Create an issue first** for significant changes
2. **Write tests** for new functionality
3. **Update documentation** if needed
4. **Follow existing code style**
5. **Keep PRs focused** - one feature or fix per PR

### PR Checklist

- [ ] Tests pass locally
- [ ] Linting passes
- [ ] Documentation updated (if applicable)
- [ ] Commit messages are clear and descriptive
- [ ] PR description explains the change

## Commit Messages

Use clear, descriptive commit messages:

```
feat: add streak calculation to dashboard
fix: resolve encryption key derivation issue
docs: update API documentation for journal endpoints
test: add integration tests for magic link auth
```

## Architecture Guidelines

- **API-first**: All features are DRF endpoints first
- **Encryption**: Journal entries must remain encrypted at rest
- **Bilingual**: Content should support en/es from the start
- **Privacy**: Never expose private journal content through group endpoints

## Questions?

Open an issue or reach out to the maintainers.
