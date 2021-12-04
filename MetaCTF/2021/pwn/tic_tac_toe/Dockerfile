FROM debian:buster-20200803

RUN apt-get update -y && apt-get install xinetd -y

RUN mkdir -p /chall

ADD chall.sh /chall
ADD chall /chall
ADD flag.txt /chall
ADD init.sh /bin
ADD chall.xinetd /etc/xinetd.d/chall

RUN groupadd -r chall && useradd -r -g chall chall && \
    chown -R root:chall /chall && \
    chmod 750 /chall/chall.sh && \
    chmod 750 /chall/chall && \
    chmod 440 /chall/flag.txt && \
    chmod 700 /bin/init.sh

RUN service xinetd restart

ENTRYPOINT [ "/bin/init.sh" ]

