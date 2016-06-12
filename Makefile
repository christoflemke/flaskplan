init:
	pip install -r requirements.txt


run:
	python run.py

build-docker:
	docker build -t flaskplan .

run-docker: build-docker
	docker run -d -p 8000:80 --name flaskplan flaskplan /usr/sbin/apache2ctl -D FOREGROUND

stop-docker:
	docker stop flaskplan
	docker rm flaskplan