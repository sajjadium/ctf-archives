FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y libcurl4-openssl-dev \
    curl npm
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

COPY src /app
COPY run.sh /
COPY readflag /
COPY flag /
RUN chmod 400 /flag && chmod +x run.sh readflag && chmod +s /readflag 
RUN cd /app && npm install --build-from-source

ENTRYPOINT [ "/run.sh" ]

