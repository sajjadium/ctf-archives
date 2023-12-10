FROM ubuntu:22.04
RUN apt update && apt -y upgrade
RUN apt install -y xinetd
RUN useradd -u 10000 -m ctf

RUN apt install -y python3 python3-pip
RUN pip3 install unicorn gmpy2

COPY ./xinetd.conf /etc/xinetd.d/ctf
COPY ./run.sh /
COPY ./server.py /
COPY ./secret.py /
COPY ./pow.py /

RUN chmod +x /run.sh

CMD ["/usr/sbin/xinetd", "-dontfork"]

EXPOSE 23230
