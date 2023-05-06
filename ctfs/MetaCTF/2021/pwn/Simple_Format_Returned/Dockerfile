FROM debian:buster-20200803

RUN apt-get update -y && apt-get install xinetd gdb -y 

RUN mkdir -p /fundamentals

ADD fundamentals.sh /fundamentals
ADD fundamentals /fundamentals
ADD flag.txt /fundamentals
ADD flag2.txt /fundamentals
ADD init.sh /bin
ADD fundamentals.xinetd /etc/xinetd.d/fundamentals

RUN groupadd -r fundamentals && useradd -r -g fundamentals fundamentals && \
    chown -R root:fundamentals /fundamentals && \
    chmod 750 /fundamentals/fundamentals.sh && \
    chmod 750 /fundamentals/fundamentals && \
    chmod 440 /fundamentals/flag.txt && \
    chmod 440 /fundamentals/flag2.txt && \
    chmod 700 /bin/init.sh

RUN service xinetd restart

ENTRYPOINT [ "/bin/init.sh" ]

