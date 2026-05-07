# Contributing to Devotional Journal

Thanks for being here. This project is built by men, for men trying to be more consistent in their faith — and contributions from anyone who wants to make that happen are welcome.

If you're new to open-source, that's fine. Open an issue, ask questions, and pair on a small fix. Drive-by typo fixes in docs are perfectly valid PRs.

## Code of Conduct

Be respectful, inclusive, and constructive. This project serves a faith-based community, and we expect everyone here to treat each other with the dignity that implies.

Disagreements are welcome. Personal attacks, harassment, and gatekeeping by tradition or denomination are not.

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
- **Bilingual**: Content should support en/es from the start, including proper diacritics in Spanish (`Configuración`, not `Configuracion`)
- **Privacy**: Never expose private journal content through group endpoints
- **No third-party trackers**: Do not add Google Analytics, Facebook pixels, or similar without explicit operator opt-in
- **Accessibility**: New UI must keep keyboard navigation, semantic landmarks, and ARIA labels working — see the skip-link and `aria-current` patterns in `Layout.tsx`

## Documentation expectations

If your PR adds or changes user-visible behavior:

1. Update the relevant docs (README features list, ROADMAP, etc.)
2. Add a line to the `[Unreleased]` section of `CHANGELOG.md`
3. If it changes data handling, update `PRIVACY.md`
4. If it changes a security boundary, update `SECURITY.md`

## Questions?

Open an issue or start a discussion on GitHub. PRs without an associated issue are fine for small fixes; please open an issue first for anything larger.
