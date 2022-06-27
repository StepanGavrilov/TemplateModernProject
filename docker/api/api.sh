#!/bin/bash
countur=$1

echo StartUp script

rm -rf .env && ./docker/env.sh "$countur" >>.env

# shellcheck disable=SC2046
if [ "$countur" = "Local" ]; then
  source .env
else
  . /.env
fi

poetry install

# migrations
poetry run alembic revision --autogenerate -m 'initial'
poetry run alembic upgrade head

echo api start on "$API_HOST":"$API_PORT"
poetry run uvicorn asgi:app --reload --host "$API_HOST" --port "$API_PORT"

