FROM ubuntu:22.04

RUN apt update -y && apt install -y xinetd

RUN echo "You have been blocked by xinetd." > /etc/banner_fail

WORKDIR /ctf
RUN useradd -d /ctf -m ctf
COPY database ./database
COPY flag ./db/flag
COPY db /ctf/db
COPY ctf.xinetd /etc/xinetd.d/ctf
COPY scripts/init.sh /init.sh
COPY scripts/run.sh /ctf/run.sh

RUN chmod +x /ctf/database /init.sh /ctf/run.sh

ENTRYPOINT ["/init.sh"]

EXPOSE 1337

