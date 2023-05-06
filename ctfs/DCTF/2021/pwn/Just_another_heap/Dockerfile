FROM ubuntu:18.04
RUN apt-get update && apt-get install -y make gcc socat

RUN groupadd pilot
RUN useradd pilot --gid pilot

COPY ./app /app
WORKDIR /app

ENTRYPOINT [ "bash", "/app/startService.sh" ]
