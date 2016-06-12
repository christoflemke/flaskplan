FROM ubuntu:latest
MAINTAINER Christof Lemke "christof.lemke@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential libapache2-mod-wsgi apache2
RUN pip install --upgrade pip
COPY flaskplan.wsgi /var/www/flaskplan/flaskplan.wsgi
COPY cfg/flaskplan.conf /etc/apache2/sites-available/flaskplan.conf
COPY . /var/www/flaskplan/
WORKDIR /var/www/flaskplan/
RUN pip install -r requirements.txt
RUN a2enmod wsgi
RUN a2ensite flaskplan
RUN a2dissite 000-default
RUN apt-get install -y curl less
#ENTRYPOINT ["python"]
CMD ["apachectl" "-D" "FOREGROUND"]
