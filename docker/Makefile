.RECIPEPREFIX := >
.PHONY: build up down logs run ssh conecta_app

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
>$(COMPOSE) run --rm app python3 $(script)
ssh:
>@ssh root@localhost -p 22
conecta_app:
>@$(COMPOSE) exec app bash
