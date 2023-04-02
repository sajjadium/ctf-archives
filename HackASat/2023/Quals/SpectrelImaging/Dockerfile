FROM ubuntu:jammy
ARG DEBIAN_FRONTEND=noninteractive

ARG TZ=Etc/UTC


RUN apt update && \ 
    apt install bzip2

WORKDIR /challenge/
COPY ImagerScheduler .
COPY challenge.sh .
COPY stars.csv .
RUN chmod +x challenge.sh
VOLUME /data/
RUN useradd -ms /bin/bash challenge
RUN chown challenge /challenge

RUN mkdir /fpga/
RUN chown challenge /fpga 

USER challenge
CMD ./challenge.sh
