FROM ubuntu:20.04

RUN sed -i 's/archive.ubuntu.com/ftp.daumkakao.com/g' /etc/apt/sources.list

RUN groupadd -g 1000 web
RUN useradd -g web -s /bin/bash web

RUN apt update
RUN apt install -y python3 python3-pip
COPY src /srv
COPY cert.pem /srv
RUN chmod a+rw /srv/database /srv/database/sql.db 

WORKDIR /srv
RUN pip3 install -r requirements.txt
USER web

CMD python3 app.py