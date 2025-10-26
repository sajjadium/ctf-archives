FROM ubuntu:22.04

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y xinetd libicu-dev python3 python3-pip

RUN useradd -m ctf && \
    useradd -m flag

WORKDIR /home/ctf

COPY ./xinetd.conf /etc/xinetd.d/ctf
COPY ./start.sh /start.sh

RUN chmod +x /start.sh

COPY ./d8 /home/ctf/
COPY ./icudtl.dat /home/ctf/
COPY ./snapshot_blob.bin /home/ctf/
COPY ./flag /home/ctf/
COPY ./getflag /home/ctf/
COPY ./run.sh /
COPY ./server.py /

RUN chmod +x /run.sh
RUN chmod +x /server.py

RUN chown -R ctf:ctf /home/ctf && \
    chmod -R 750 /home/ctf && \
    chown root:flag /home/ctf/flag && \
    chmod 440 /home/ctf/flag && \
    chown ctf:flag /home/ctf/getflag && \
    chmod 2755 /home/ctf/getflag

CMD ["/start.sh"]

EXPOSE 7000
