up: 
	docker-compose up

upd:
	docker-compose up -d
	
upb:
	docker-compose up --build
	
updb:
	docker-compose up -d --build

build:
	docker-comopse build

down:
	docker-compose down --remove-orphans

stop:
	docker-compose stop
