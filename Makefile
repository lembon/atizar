build:
	docker compose -f docker-compose-prod.yml build 

up:
	docker compose -f docker-compose-prod.yml up -d

logs:
	docker compose -f docker-compose-prod.yml logs -f -t

migrate:
	docker compose run web ./manage.py migrate

shell:
	docker compose run web ./manage.py shell

collectstatic:
	docker compose run web ./manage.py collectstatic

createsuperuser:
	docker compose run web ./manage.py createsuperuser

down:
	docker compose -f docker-compose-prod.yml down