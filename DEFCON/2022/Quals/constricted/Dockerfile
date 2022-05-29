FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y

WORKDIR /challenge
COPY boa boa
RUN adduser --no-create-home --disabled-password --gecos "" user

USER user
CMD ["/challenge/boa"]
