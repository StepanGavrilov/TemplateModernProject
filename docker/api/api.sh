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
poetry run uvicorn asgi:app --reload --host "$API_HOST" --port "$API_PORT"
uvicorn asgi:app --reload --host "$API_HOST" --port "$API_PORT"
