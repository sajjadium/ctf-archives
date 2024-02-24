FROM python:alpine

WORKDIR /usr/src/app

COPY ./app/ .

RUN apk --no-cache add nginx supervisor && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/cache/apk/*

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 3000

ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
