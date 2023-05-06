FROM ubuntu:18.04

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y xinetd libicu-dev

RUN useradd -m ctf && \
    useradd -m flag

WORKDIR /home/ctf

RUN cp -R /lib* /home/ctf && \
    mkdir /home/ctf/usr && \
    cp -R /usr/lib* /home/ctf/usr

RUN mkdir /home/ctf/dev && \
    mknod /home/ctf/dev/null c 1 3 && \
    mknod /home/ctf/dev/zero c 1 5 && \
    mknod /home/ctf/dev/random c 1 8 && \
    mknod /home/ctf/dev/urandom c 1 9 && \
    chmod 666 /home/ctf/dev/* && \
    mkdir /home/ctf/proc

RUN mkdir /home/ctf/bin && \
    cp /bin/sh /home/ctf/bin && \
    cp /bin/ls /home/ctf/bin && \
    cp /bin/cat /home/ctf/bin && \
    cp /bin/bash /home/ctf/bin && \
    cp /usr/bin/timeout /home/ctf/bin

COPY ./xinetd.conf /etc/xinetd.d/ctf
COPY ./start.sh /start.sh

RUN chmod +x /start.sh

RUN mkdir /home/ctf/tmp

COPY ./ch /home/ctf/
COPY ./flag /home/ctf/
COPY ./getflag /home/ctf/
COPY ./run.sh /home/ctf/
RUN chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf && \
    chown root:flag /home/ctf/flag && \
    chmod 740 /home/ctf/flag && \
    chown root:flag /home/ctf/getflag && \
    chmod 2755 /home/ctf/getflag

CMD ["/start.sh"]

EXPOSE 7000