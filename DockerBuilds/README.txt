
## TO RUN

docker-compose up

## PORTS:
## rabbitmq management - 8080 -- user=guest, pass=guest
## adminer - 8010 ---> server:postgres, user:posgres, pass:secret, db:domotics - Web Access to database
## dashboard - 8888 --> for tomcat management user:domotics pass:domotics
	     - 8888/admin-stater --> dashboard webpage



## SE QUISEREM CORRER UM A UM
## DASHBOARD
## NEEDS .war FILE PRODUCED FORM mvn package OF THE DASHBOARD. admin-starter.war
1. build image in dockerfile directory:
	docker build -t <tagtoaddimage> .

2. run image in a container
 	docker run -d -p 8000:8080 --name <nome_a_dar> <tagdaimagem>

## RABBITMQ
	docker run -d -p 8080:15672 --name <nome_a_dar> rabbitmq

## POSTGRESQL comunicating port 5432; adminer 8010;
