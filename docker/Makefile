.RECIPEPREFIX := >
.PHONY: build up down logs run

COMPOSE = docker compose --env-file ./.env

build:
>$(COMPOSE) build

up:
>$(COMPOSE) up -d

down:
>$(COMPOSE) down

logs:
>$(COMPOSE) logs -f

run:
>$(COMPOSE) run --rm app python $(script)
