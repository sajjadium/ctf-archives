FROM python:3.10.12-slim-bullseye AS app

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y gcc make

COPY ./readflag.c /readflag.c

RUN gcc /readflag.c -o /readflag

RUN rm /readflag.c

RUN chmod 701 /readflag

RUN pip install asteval==1.0.5
# apply patches to asteval
COPY ./astutils.py.patched /usr/local/lib/python3.10/site-packages/asteval/astutils.py
COPY ./asteval.py.patched /usr/local/lib/python3.10/site-packages/asteval/asteval.py
WORKDIR /challenge
COPY chal.py .
RUN useradd -u 1000 ctfuser

FROM pwn.red/jail

COPY --from=app / /srv
RUN mkdir -p /srv/app
COPY --chmod=555 ./run /srv/app/run

ENV JAIL_PIDS=40 JAIL_MEM=25M JAIL_TIME=120