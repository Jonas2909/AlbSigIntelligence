# Guide for Live Enviroment

## commands:

### building the docker container
```
sudo docker build -t docker-arp .
```
### running the docker container
```
sudo docker run -it --network host --name docker-arp docker-arp
```
### stopping the docker container 
```
sudo docker ps -a

sudo docker stop <ID>

sudo docker rm <ID>
```

## Steps that need to be done prior

* start RestService
* start Visualization

