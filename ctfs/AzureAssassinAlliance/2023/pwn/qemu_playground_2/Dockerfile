FROM ubuntu:22.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
    apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y lib32z1 xinetd \
                       libpixman-1-dev libepoxy-dev libpng16-16 libjpeg8-dev \
                       libfdt-dev libnuma-dev libglib2.0-dev \
                       libgtk-3-dev libasound2-dev libcurl4

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
    cp /bin/sh /home/ctf/bin && \
    cp /bin/ls /home/ctf/bin && \
    cp /bin/cat /home/ctf/bin && \
    cp /bin/timeout /home/ctf/bin

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./start.sh /start.sh
COPY ./env /home/ctf/

RUN chmod +x /start.sh
RUN chown -R root:ctf /home/ctf && chmod -R 750 /home/ctf && chmod 740 /home/ctf/flag

CMD ["/start.sh"]

EXPOSE 9999
