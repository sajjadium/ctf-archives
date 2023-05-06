FROM node:latest

RUN groupadd -r web && useradd web -g web && mkdir /home/web && chown -R web:web /home/web

USER web

ENTRYPOINT /web/entrypoint.sh