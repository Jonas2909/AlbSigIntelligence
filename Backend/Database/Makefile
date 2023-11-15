DATABASE_NAME ?= local_postgres
SERVICE_NAME ?= example_image
NETWORK_NAME ?= localnetwork
PLATFORM_NAME ?= linux/arm/v7

DB_NAME = exampledb
DB_PASSWORD ?= mysecretpassword
DB_PORT ?= 5432

CONTAINER_NAME_SERVICE = base
CONTAINER_NAME_DB ?= local_db

build_all:
	docker run --privileged --rm tonistiigi/binfmt --install all

	docker build --tag ${DATABASE_NAME} ./

	docker network create ${NETWORK_NAME}

run_db:
	docker run --name=${CONTAINER_NAME_DB} --net=${NETWORK_NAME} -e POSTGRES_PASSWORD=${DB_PASSWORD} -e POSTGRES_DB=${DB_NAME} -d -p ${DB_PORT}:${DB_PORT} ${DATABASE_NAME}

execute_db:
	docker exec -it ${CONTAINER_NAME_DB} psql -d ${DB_NAME} -U postgres
