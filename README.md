# AI Text Analyzer

A production-style AI text analysis API — Phase 1 of the AI Engineer roadmap.

## What this is

A FastAPI service that analyzes text input and returns a summary, word count, and sentiment. Currently uses rule-based logic; in Phase 2, the internals get swapped for LLM API calls while the endpoint interface stays the same.

## Why it's built this way

This project exists to practice **how real engineering teams ship software**, not just to analyze text. Every choice here mirrors what you'd see at a real company:

- **Pydantic models** for request/response validation (not raw dicts)
- **Structured logging** with context (not print statements)
- **Health check endpoint** (every production service has one)
- **Tests before shipping** (8 tests covering happy path + edge cases)
- **CI pipeline** (GitHub Actions runs lint + tests on every push)
- **Docker support** (containerized for consistent deployment)
- **Type hints everywhere** (mypy-compatible)

## Architecture decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Framework | FastAPI | Industry default for Python AI services; async, auto-docs, Pydantic integration |
| Validation | Pydantic v2 | Type-safe, auto-generates OpenAPI schema, catches bad input before it hits your logic |
| Logging | stdlib logging | No extra dependency; structured enough for this stage, swap for structlog later |
| Testing | pytest | Industry standard; cleaner than unittest |
| Linting | ruff | Fast, replaces flake8+isort+black in one tool |

## Getting started

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn src.app.main:app --reload

# Run tests
pytest tests/ -v

# Lint
ruff check src/ tests/

# Docker
docker build -t ai-analyzer .
docker run -p 8000:8000 ai-analyzer
```

## API

Once running, open `http://localhost:8000/docs` for interactive API docs.

**POST /analyze**
```json
{
  "text": "The new product launch exceeded our Q3 targets by 40%."
}
```

Response:
```json
{
  "summary": "The new product launch exceeded our Q3 targets by 40%.",
  "word_count": 11,
  "sentiment": "positive",
  "processed_at": "2026-08-30T12:00:00Z"
}
```

## What's next (Phase 2)

- [ ] Replace rule-based sentiment with OpenAI/Anthropic API call
- [ ] Add prompt engineering for structured extraction
- [ ] Add response caching and cost tracking
- [ ] Deploy to Render/Railway free tier
