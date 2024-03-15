up: 
	docker-compose up
upd:
	docker-compose up -d
upb:
	docker-compose up --build
updb:
	docker-compose up -d --build
build:
	docker-compose build
down:
	docker-compose down --remove-orphans
stop:
	docker-compose stop
log:
	docker-compose logs back
test:
	ruff check app && docker-compose exec back python -m pytest tests -s
