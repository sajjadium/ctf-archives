FROM python:3.11.3-slim-bullseye as app
RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y gcc make

COPY ./readflag.c /readflag.c

RUN gcc /readflag.c -o /readflag

RUN rm /readflag.c

RUN chmod 701 /readflag

WORKDIR /challenge

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY chal.py .
COPY template .
COPY test.cfg .

RUN useradd -u 1000 ctfuser

FROM pwn.red/jail

COPY --from=app / /srv
RUN mkdir -p /srv/app
COPY --chmod=555 ./run /srv/app/run

ENV JAIL_PIDS=40 JAIL_MEM=100M JAIL_TIME=120