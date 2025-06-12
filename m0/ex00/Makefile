default: up

up:
	@docker compose -f ./compose.yml up

stop:
	@docker compose -f ./compose.yml stop

down:
	@docker compose -f ./compose.yml down

build:
	@docker compose -f ./compose.yml build

fclean:
	@docker compose -f ./compose.yml down -v --rmi all
	@docker system prune -af

.PHONY: build
