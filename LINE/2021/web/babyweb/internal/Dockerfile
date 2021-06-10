FROM ubuntu:20.04

RUN sed -i 's/archive.ubuntu.com/ftp.daumkakao.com/g' /etc/apt/sources.list

RUN groupadd -g 1000 web
RUN useradd -g web -s /bin/bash web

RUN apt update
RUN apt install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
RUN apt-get install -y nodejs

ADD ./src/ /srv
ADD key.pem /srv
ADD cert.pem /srv
RUN chmod 604 /srv/key.pem

WORKDIR /srv
RUN npm install
USER web

CMD npm start
