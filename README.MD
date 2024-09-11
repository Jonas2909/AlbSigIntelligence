# AlbSigIntelligence

Project of Moritz Butzke, Maximilian Englert and Jonas Reinecke

## Run Database as Docker Container manually

Install build support for additional platforms: <br> 
docker run --privileged --rm tonistiigi/binfmt --install all <br>

Building Database Container (folder: Backend): <br>
docker build -t "local_postgres" . <br>
 
Create Docker Network: <br>
docker network create localnetwork <br>

Start Database Container: <br>
docker run --name=local_db --net=localnetwork -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=exampledb -d -p 5432:5432 local_postgres <br>

Connect to Database: <br>
docker exec -it local_db psql -d exampledb -U postgres <br>

## Run Database as Docker Container using Makefile

Build Database Container and create Docker Network: <br>
make build_all <br>

Run Database as Docker Container using Makefile: <br>
make run_db <br>

Connect to Database Container: <br>
make execute_db <br>

## Run Python RestService manually

Run RestService using CLI: <br>
flask --app RestService.py run <br>

Rest-Request are added as JSON-File in folder "Routes" and can be imported into Postman <br>

RestService runs on localhost:5000 on default <br>

List of implemented and working Requests: <br>
/Hello <br>
/GetAllUsers <br>
/GetUser <br>
/AddUser <br>
/DeleteUser <br>

## Run Python RestService as Docker Container manually

Location Folder: /RestService

Build RestService as Docker Container manually: <br>
docker build -t flask-rest-api . <br>

Run RestService as Docker Container manually: <br>
docker run --name=flask-rest-api --net=localnetwork -d -p 5000:5000 flask-rest-api <br>

Routes on RestService are noch reachable as shown above, but RestService is running as Docker Container instead of locally <br>

## Run Python RestService as Docker Container using Makefile

Location Folder: /RestService

Build RestService Container: <br>
make build_rest_service <br>

Run RestService as Docker Container using Makefile: <br>
make run_rest_service <br>

Show Logs of RestService: <br>
make show_logs <br>


## Run Database and RestService as Docker Container using docker-compose

Location Folder: /Test-DockerCompose

Build and Run Database and RestService as Docker Container using docker compose: <br>
docker-compose up --build

If the Image are already built you only need to run them: <br>
docker-compose up <br> 
