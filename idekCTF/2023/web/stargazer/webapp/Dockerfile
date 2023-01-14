FROM golang:1.19-bullseye

RUN apt update 
RUN apt install -y apache2 curl
RUN apt install -y apache2-utils
RUN apt install -y supervisor

WORKDIR /app

COPY ./go/go.mod .
COPY ./go/go.sum .
RUN go mod download
COPY ./go/*.go ./
COPY ./go/public /app/public
COPY ./go/uploads /app/uploads
RUN go build -o /stargazer

COPY ./httpd/stargazer.conf /etc/apache2/sites-enabled/000-default.conf
RUN apt clean
RUN a2enmod proxy
RUN a2enmod proxy_http
COPY ./httpd/html/index.html /var/www/html/index.html

COPY ./webapp.conf /etc/supervisor/conf.d/stargazer.conf

CMD ["/usr/bin/supervisord"]