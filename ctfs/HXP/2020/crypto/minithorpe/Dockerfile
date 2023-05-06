# echo 'hxp{FLAG}' > flag.txt && head -c 32 /dev/urandom > server-secret && docker build -t minithorpe . && docker run --cap-add=SYS_ADMIN --security-opt apparmor=unconfined -ti -p 8831:80 minithorpe

FROM debian:buster
ARG WORKERS=16

RUN apt-get update && \
    apt-get install -y nginx python3 python3-pip && \
    rm -rf /var/lib/apt/lists/

RUN pip3 install flask gunicorn

COPY ynetd /sbin/
RUN chmod 500 /sbin/ynetd

RUN rm -rf /var/www/html/*
COPY docker-stuff/default /etc/nginx/sites-enabled/default

COPY flag.txt /flag.txt
RUN chown root:root /flag.txt && \
    mv flag.txt flag_$(< /dev/urandom tr -dc a-zA-Z0-9 | head -c 24).txt && \
    chmod 444 /flag_*.txt

RUN mkdir /var/www/app/
COPY index.html /var/www/html/
COPY octothorpe.py service.py executor.py /var/www/app/
RUN chown -R root:root /var/www && \
    find /var/www -type d -exec chmod 555 {} \; && \
    find /var/www -type f -exec chmod 444 {} \; && \
    chmod 005 /var/www/app/executor.py

COPY server-secret /server-secret
RUN chown root:www-data /server-secret && \
    chmod 040 /server-secret

RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

USER www-data
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock|/var/log/nginx/error.log|/var/log/nginx/access.log|/server-secret)'

USER root
RUN useradd --no-create-home --shell /bin/bash ctf

USER ctf
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock|/var/log/nginx/error.log|/var/log/nginx/access.log)'

USER root

EXPOSE 80
ENV GUNICORN_WORKERS $WORKERS
ENV PYTHONDONTWRITEBYTECODE 1
CMD ynetd -lt 1 -t 2 -sh n -lpid 16 -a 127.0.1.1 -d /var/www/app /var/www/app/executor.py & \
    gunicorn --chdir /var/www/app --workers "$GUNICORN_WORKERS" --preload --bind unix:/var/www/app.sock --user www-data --group www-data --umask 027 service:app & \
    nginx -g 'daemon off;'
