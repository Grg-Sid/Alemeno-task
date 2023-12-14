# syntax=docker/dockerfile:1

# Stage 1: Base stage
ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

USER appuser

COPY . .

EXPOSE 8000

CMD gunicorn '.venv.lib.python3.10.site-packages.asgiref.wsgi' --bind=0.0.0.0:8000

# Stage 2: Celery worker stage
FROM base as celery

USER root

# Install additional dependencies for Celery (e.g., Redis as a message broker)
RUN apt-get update && apt-get install -y \
    rabbitmq-server

USER appuser

# Run the Celery worker
CMD celery -A loan worker --loglevel=info