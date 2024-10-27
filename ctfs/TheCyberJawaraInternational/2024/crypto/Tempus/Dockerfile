FROM python:3.8-slim

RUN apt-get update
RUN apt-get install -y nano socat gcc
RUN pip install ethsnarks

WORKDIR /opt

COPY challenge.py .
COPY flag.txt .

CMD socat TCP-LISTEN:5000,fork,reuseaddr EXEC:'python3 challenge.py'