NETWORK_NAME ?= localnetwork
SERVICE_NAME ?= flask-rest-api
SERVICE_PORT ?= 5000

build_rest_service:
	docker build -t ${SERVICE_NAME} .

run_rest_service:
	docker run --name= ${SERVICE_NAME} --net= ${NETWORK_NAME} -d -p ${SERVICE_PORT}:${SERVICE_PORT} ${SERVICE_NAME} 

show_logs:
	docker logs ${SERVICE_NAME}
