FROM python:3

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /usr/src/app

RUN apt update
RUN apt install cron -y
RUN pip install pwntools

COPY ./admin_janitor.py .
COPY ./cron .
COPY ./entrypoint.sh .

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]