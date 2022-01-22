FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update &&\
    apt-get install -y --no-install-recommends gcc g++ cmake make wget unzip socat

WORKDIR /app/

RUN wget --no-check-certificate https://github.com/parrt/simple-virtual-machine-C/archive/refs/heads/master.zip -O svme.zip &&\
    unzip svme.zip
COPY ./main.c /app/simple-virtual-machine-C-master/src/vmtest.c
RUN  cd simple-virtual-machine-C-master &&\
    cmake . &&\
    make &&\
    mv ./simple_virtual_machine_C /app/svme &&\
    cd /app/ &&\
    rm -rf ./simple-virtual-machine-C-master

RUN useradd --no-create-home -u 1000 user
COPY flag /

CMD ["socat", "tcp-l:1337,reuseaddr,fork,su=user", "exec:/app/svme"]


