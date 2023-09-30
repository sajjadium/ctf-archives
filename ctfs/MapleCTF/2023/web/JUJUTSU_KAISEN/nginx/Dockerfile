FROM nginx:1.25.2-alpine

RUN mkdir -p /etc/nginx/ssl

RUN apk upgrade --update-cache --available && \
    apk add openssl

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/nginx.key \
    -out /etc/nginx/ssl/nginx.crt \
    -subj "/C=CA/ST=BC/L=Vancouver/O=Omegalul/CN=www.maplebacon.org"

COPY ./default.conf /etc/nginx/conf.d/

CMD ["nginx", "-g", "daemon off;"]




