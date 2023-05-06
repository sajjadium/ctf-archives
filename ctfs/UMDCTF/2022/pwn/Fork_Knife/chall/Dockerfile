FROM ubuntu:20.04

RUN apt update -y && apt install -y \
    xinetd

RUN useradd -u 1000 uncool
RUN useradd -u 1001 cool
RUN mkdir /ctf
RUN echo "You have been blocked by xinetd. Report this to the organizers if this persists." > /etc/banner_fail

COPY ./scripts/init.sh /init.sh
COPY ./scripts/run.sh /ctf/run.sh
COPY ./scripts/clean.sh /ctf/clean.sh
COPY ./scripts/crontab /etc/crontab
COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./fnk /ctf/fnk
COPY ./flag.txt /ctf/flag.txt

RUN chown -R root:uncool /ctf && chmod -R 744 /ctf/*
RUN chown root:cool /ctf/flag.txt && chmod 740 /ctf/flag.txt # no flag for u :)
RUN chmod 733 /tmp # only allow writing to /tmp

RUN chmod +x /init.sh /ctf/run.sh /ctf/clean.sh /ctf/fnk

CMD ["/init.sh"]

EXPOSE 1447
