FROM --platform=linux/amd64 amd64/ubuntu:22.04

RUN apt update -y && apt install -y xinetd

RUN echo "You have been blocked by xinetd. Report this to the organizers if this persists." > /etc/banner_fail

WORKDIR /ctf
RUN useradd -d /ctf -m ctf
COPY bbfmspmss ./bbfmspmss
COPY flag.txt ./flag.txt
COPY ctf.xinetd /etc/xinetd.d/ctf
COPY scripts/init.sh /init.sh
COPY scripts/run.sh /ctf/run.sh

RUN mkdir ./boxes
RUN mkdir ./db
RUN chmod 1777 ./db ./boxes

RUN chmod +x /ctf/bbfmspmss /init.sh /ctf/run.sh

ENTRYPOINT ["/init.sh"]

EXPOSE 1447

