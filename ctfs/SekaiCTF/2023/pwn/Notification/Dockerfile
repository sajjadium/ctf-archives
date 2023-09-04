FROM ubuntu:22.04

RUN apt update -y && apt install -y xinetd

RUN echo "You have been blocked by xinetd." > /etc/banner_fail

WORKDIR /ctf
RUN useradd -d /ctf -m ctf
COPY notification ./notification
COPY libzone.so ./libzone.so
COPY flag.txt ./flag.txt
COPY ctf.xinetd /etc/xinetd.d/ctf
COPY scripts/init.sh /init.sh
COPY scripts/run.sh /ctf/run.sh

RUN chmod +x /ctf/notification /ctf/libzone.so /init.sh /ctf/run.sh

ENTRYPOINT ["/init.sh"]

EXPOSE 1337

