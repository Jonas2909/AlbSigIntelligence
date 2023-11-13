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
<br>make execute_db <br>

## Run Python RestService

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



