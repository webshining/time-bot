run:
	python main.py
compose:
	docker-compose up -d
rebuild: 
	docker-compose up -d --build --no-deps --force-recreate