FROM liferay/portal:7.0.6-ga7
MAINTAINER peterjson

USER root
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y nginx supervisor

COPY ./container/adminPortal/supervisor.conf /etc/supervisor.conf

# I implement my own rule to protect our admin portal

RUN rm /etc/nginx/sites-available/default && rm /etc/nginx/sites-enabled/default

COPY ./container/adminPortal/default /etc/nginx/sites-available/

RUN ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

COPY ./container/adminPortal/flag.txt ./container/adminPortal/readflag /

RUN chown 0:1337 /flag.txt /readflag && \
    chmod 040 /flag.txt && \
    chmod 2555 /readflag

ENTRYPOINT ["supervisord", "-c", "/etc/supervisor.conf"]

EXPOSE 80