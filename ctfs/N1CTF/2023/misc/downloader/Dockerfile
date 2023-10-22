FROM ctfhub/pwn_xinetd

COPY files/start.sh /start.sh
COPY files/flag.sh /flag.sh
COPY files/readflag /readflag
COPY src /app
RUN apt update &&\
    apt install wget -y &&\
    apt clean all &&\
    rm -rf /var/lib/apt/lists/* 

RUN rm -rf /etc/alternatives/*
