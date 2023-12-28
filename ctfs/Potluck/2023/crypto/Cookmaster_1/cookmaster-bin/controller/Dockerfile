FROM debian:bookworm-20231218
ENV DEBIAN_FRONTEND noninteractive
RUN set -ex;\
    apt-get update;\
    apt-get install -y libssl3

WORKDIR /app
COPY ./controller/controller .
COPY ./controller/run.sh .
COPY wait_for_can.sh .
COPY privkey .
COPY recipes.json . 
COPY flag1 flag
CMD ./run.sh
