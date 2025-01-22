FROM node:20-bullseye-slim AS app

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y gcc make

COPY ./readflag.c /readflag.c

RUN gcc /readflag.c -o /readflag

RUN rm /readflag.c

RUN chmod 701 /readflag

RUN mkdir -p /challenge
WORKDIR /challenge
COPY package.json .
COPY chal.js .
RUN npm install

FROM pwn.red/jail

COPY --from=app / /srv
RUN mkdir -p /srv/app
COPY --chmod=555 ./run /srv/app/run

ENV JAIL_PIDS=40 JAIL_MEM=100M JAIL_TIME=120
