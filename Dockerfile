# syntax=docker/dockerfile:1

# Stage 1: Base stage
ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

USER appuser

COPY . .


FROM base as celery

USER root

# Install additional dependencies for Celery
RUN apt-get update && apt-get install -y \
    rabbitmq-server

USER appuser

# Run the Celery worker
CMD celery -A loan worker --loglevel=info