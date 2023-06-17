FROM ubuntu:18.04

# Base install
RUN apt update
RUN apt install locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV DEBIAN_FRONTEND noninteractive
RUN apt install -y wget unzip build-essential cmake gcc libcunit1-dev libudev-dev socat netcat net-tools inetutils-ping

# For service
COPY service /service
RUN chown -R root:root /service
RUN chmod -R 555 /service

# Flag
COPY flag.txt /flag.txt

# Finishing
WORKDIR /service
RUN useradd ctf
EXPOSE 8000
ENTRYPOINT ["socat", "TCP4-LISTEN:8000,reuseaddr,fork,su=ctf", "EXEC:'./airport_system'"]