FROM python:3.10-slim-buster

COPY ../.. .

RUN \
    sed -i -e's/ main/ main contrib non-free/g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    liblzo2-dev \
    libmagic1 \
    p7zip-full \
    p7zip-rar \
    make \
    git \
    nano \
    build-essential \
    && rm -rf /var/lib/apt/lists/*  \
    && pip install --upgrade pip \
    && pip install poetry
