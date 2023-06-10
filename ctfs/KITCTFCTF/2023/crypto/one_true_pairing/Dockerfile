# docker build -t one-true-pairing . && docker run -p 1337:1337 one-true-pairing
# stub the unknown parts from secret.py with reasonable replacements to test locally

FROM python:3.9-slim

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat

RUN adduser --disabled-password --gecos "" user

WORKDIR /challenge/

COPY main.py secret.py ./

USER user
EXPOSE 1337

ENTRYPOINT [ "socat", "tcp-l:1337,reuseaddr,fork", "exec:python3 ./main.py" ]
