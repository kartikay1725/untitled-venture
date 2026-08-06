# MVPGenie Backend

Production‑ready FastAPI backend implementing secure authentication, idea validation, and MVP blueprint generation.

## Features
- JWT authentication with refresh token rotation
- Rate limiting & WAF‑style request throttling
- Security headers (CSP, HSTS, X‑Frame‑Options)
- Input validation & sanitization
- Audit logging to immutable file
- Unit & integration tests
- Dockerized deployment

## Setup
```bash
cp .env.example .env
# set environment variables
uvicorn app.main:app --reload
```
