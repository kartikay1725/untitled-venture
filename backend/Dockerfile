# syntax=docker/dockerfile:1.4
FROM python:3.12-slim as builder
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry==1.8.3
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi
RUN chmod -R 555 /app
FROM python:3.12-slim as runtime
WORKDIR /app
COPY --from=builder /app /app
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]