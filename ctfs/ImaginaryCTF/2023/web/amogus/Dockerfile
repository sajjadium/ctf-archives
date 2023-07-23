FROM nginx:latest

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip

RUN mkdir /app

COPY requirements.txt /app
RUN pip3 install --no-cache-dir --break-system-packages -r /app/requirements.txt

COPY auth /app/auth/
COPY mail /app/mail/

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY nginx/default /etc/nginx/conf.d/0default.conf
COPY nginx/mail-service /etc/nginx/conf.d/1mail-service.conf
COPY nginx/auth-service /etc/nginx/conf.d/2auth-service.conf
COPY nginx/index.html /var/www/html/index.html

EXPOSE 80

CMD ["/bin/bash", "/entrypoint.sh"]
