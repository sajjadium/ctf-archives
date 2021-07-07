FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/ftp.sjtu.edu.cn/g" /etc/apt/sources.list && \
    apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y xinetd qemu-user

RUN useradd -m ctf

WORKDIR /home/ctf

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./start.sh /start.sh
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

RUN chmod +x /start.sh

COPY ./flag /flag
COPY ./readflag /readflag
RUN chmod u+s /readflag && \
    chmod 400 /flag

COPY ./binary/ /home/ctf/
RUN chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf

RUN chmod 750 /bin/sh

RUN apt-get -y autoremove
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# USER ctf

CMD ["/start.sh"]

EXPOSE 9999
