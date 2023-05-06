FROM python:3.10-slim-buster

RUN groupadd -r web && useradd web -g web && mkdir /home/web && chown -R web:web /home/web

COPY . /web

RUN chown web:web /web

USER web

ENTRYPOINT /web/entrypoint.sh