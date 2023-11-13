# AlbSigIntelligence

School project of Moritz Butzke, Maximilian Englert and Jonas Reinecke

## Run Database as Docker Container manually

Install build support for additional platforms: 
docker run --privileged --rm tonistiigi/binfmt --install all

Building Database Container (folder: Backend): 
docker build -t "local_postgres" .
 
Create Docker Network: 
docker network create localnetwork

Start Database Container: 
docker run --name=local_db --net=localnetwork -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=exampledb -d -p 5432:5432 local_postgres

Connect to Database:
docker exec -it local_db psql -d exampledb -U postgres

## Run Database as Docker Container using Makefile

Build Database Container and create Docker Network:
make build_all

Run Database as Docker Container using Makefile:
make run_db

Connect to Database Container:
make execute_db

## Run Python RestService

Run RestService using CLI:
flask --app RestService.py run

Rest-Request are imported as JSON-File in folder "Routes" and can be imported into Postman

RestService runs on localhost:5000 on default

List of implemented and working Requests:
/Hello
/GetAllUsers
/GetUser
/AddUser
/DeleteUser



