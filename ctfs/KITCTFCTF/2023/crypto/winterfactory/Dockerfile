# docker build -t winterfactory . && docker run -p 1337:1337 winterfactory
FROM ubuntu:22.10

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update --fix-missing && apt-get upgrade -y
RUN apt-get install -y make socat python3-pip

RUN adduser --disabled-password --gecos "" user

WORKDIR /home/user/

COPY winterfactory.py winterfactory.py

EXPOSE 1337
USER user

RUN pip install winternitz

ENTRYPOINT [ "socat", "tcp-listen:1337,reuseaddr,fork", "EXEC:'timeout 60 stdbuf -i0 -o0 -e0 python3 winterfactory.py'" ]
