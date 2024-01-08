#!/bin/bash

# Inicia o aplicativo Django com build
docker compose up -d --build app

# Verifica se o contêiner Caddy está em execução
CADDY_RUNNING=$(docker ps --format '{{.Names}}' | grep -E '^[^-]+-caddy-[0-9]+$')

if [ -z "$CADDY_RUNNING" ]; then
  docker compose up -d --build caddy
fi
