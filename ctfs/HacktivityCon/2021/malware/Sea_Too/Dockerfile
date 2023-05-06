# This Dockerfile is provided for testing your solution on your local machine.

FROM ubuntu:latest

COPY flag.txt /usr/local/share

RUN useradd -u 1000 -d /home/user -s /bin/bash user

COPY runner .
COPY malware .
COPY runner .

RUN chmod 444 /usr/local/share/flag.txt
RUN chmod 555 /malware
RUN chmod 555 /runner

USER user
CMD "/runner"
