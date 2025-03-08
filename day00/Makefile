DOCKER_COMPOSE = docker-compose.yml


all:
	@docker compose -f ${DOCKER_COMPOSE} up -d --build

up:
	@docker compose -f ${DOCKER_COMPOSE} up

down:
	@docker compose -f ${DOCKER_COMPOSE} down


# # ---- Clean rules ---- #

prune:
	@docker compose -f ${DOCKER_COMPOSE} stop
	@docker system prune -a;
	@docker volume prune;

fclean:
	- @docker compose -f ${DOCKER_COMPOSE} down --rmi all -v --remove-orphans
# 	- @rm -rf backend/cert

re: down
	${MAKE} all

.PHONY: all fclean up down