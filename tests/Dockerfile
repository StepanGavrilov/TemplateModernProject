FROM python:3.10-slim-buster

RUN apt-get update \
    && apt-get install -y \
    python3-dev \
    gcc \
    libpq-dev

COPY ../.. /
COPY pyproject.toml poetry.lock ./
RUN pip install  \
    poetry && poetry install
ENV PYTHONPATH=.