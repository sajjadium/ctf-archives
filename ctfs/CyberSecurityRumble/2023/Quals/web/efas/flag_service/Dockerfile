FROM debian:bullseye

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-wheel

RUN pip3 install flask

ADD app/ /app
WORKDIR /app
ENTRYPOINT flask run --host=0.0.0.0 --port=80