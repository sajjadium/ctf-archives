FROM ubuntu:22.04

RUN apt-get update && apt-get install socat python3 python3-pip -y
RUN pip3 install pycryptodome

WORKDIR /app
COPY ./file_crypto.py /app
COPY ./remote.py /app
COPY ./key /app
COPY ./vectors /app

EXPOSE 9137

CMD ["socat", "TCP-LISTEN:9137,reuseaddr,fork", "EXEC:python3 remote.py,nofork,stderr"]