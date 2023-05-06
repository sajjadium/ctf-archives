FROM ubuntu:20.04

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3 python3-pip
RUN useradd -d /home/fword/ -m -p fword -s /bin/bash fword

COPY . /data/
WORKDIR /data
RUN pip3 install -r requirements.txt
RUN chown -R root:root /data
RUN chmod -R o+rw /data/static
USER fword
CMD /data/start.sh
