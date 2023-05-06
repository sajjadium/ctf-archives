FROM ubuntu:22.04

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y lib32z1 xinetd locales

RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

RUN useradd -m ctf

WORKDIR /home/ctf

RUN cp -R /usr/lib* /home/ctf

RUN mkdir /home/ctf/dev && \
    mknod /home/ctf/dev/null c 1 3 && \
    mknod /home/ctf/dev/zero c 1 5 && \
    mknod /home/ctf/dev/random c 1 8 && \
    mknod /home/ctf/dev/urandom c 1 9 && \
    chmod 666 /home/ctf/dev/*

RUN mkdir /home/ctf/bin && \
    mkdir /home/ctf/home && \
    mkdir /home/ctf/tmp && \
    cp /bin/sh /home/ctf/bin && \
    cp /bin/ls /home/ctf/bin && \
    cp /bin/cat /home/ctf/bin

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./start.sh /start.sh
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

RUN chmod +x /start.sh

COPY ./bin/pcg /home/ctf/
COPY ./bin/flag.txt /home/ctf/home/

RUN chown -R ctf:ctf /home/ctf && \
    chmod -R 750 /home/ctf && \
    chmod 740 /home/ctf/home/flag.txt

RUN mkdir -p /home/ctf/usr/local && \
    cp -r /usr/local/lib /home/ctf/usr/local/ && \
    cp -r /usr/lib /home/ctf/usr/

CMD ["/start.sh"]

EXPOSE 9999
