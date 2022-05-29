

FROM ubuntu:22.04 as challenge

WORKDIR /perribus/challenge
COPY  cryptochall /perribus/challenge/
COPY flag.txt /perribus/challenge/

RUN adduser --no-create-home --disabled-password --gecos "" user
USER user

CMD ["/perribus/challenge/cryptochall"]
