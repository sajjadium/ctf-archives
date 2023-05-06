FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y xinetd python3 xxd

COPY mjs /
COPY ynetd /
COPY remote.py /

RUN echo "kalmar{redacted}" > /flag-$(head -c 16 /dev/urandom | xxd -p).txt

USER 1000:1000

EXPOSE 10002

CMD ./ynetd -p 10002 "timeout 60 ./remote.py"

