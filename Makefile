init:
	pip install -r requirements.txt


run:
	python run.py

docker-build:
	docker build -t christoflemke/flaskplan .

docker-run: docker-build
	docker run -d -p 8000:80 --name flaskplan christoflemke/flaskplan /usr/sbin/apache2ctl -D FOREGROUND

docker-stop:
	docker stop flaskplan
	docker rm flaskplan
