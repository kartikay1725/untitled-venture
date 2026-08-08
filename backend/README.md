# IdeaForge Backend

FastAPI based backend for IdeaForge platform.

## Features

- User registration & login with JWT
- Idea submission & validation
- MVP blueprint generation
- Health check endpoint
- Rate limiting, structured logging, error handling

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations (create tables)
python -m backend.app.db.database --create

# Start server
uvicorn backend.main:app --reload
```

## Environment Variables

See `.env.example`.

## Testing

```bash
pytest