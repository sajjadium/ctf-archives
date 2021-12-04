FROM debian:buster-20200803

RUN apt-get update -y && apt-get install xinetd -y

RUN mkdir -p /sequential

ADD sequential.sh /sequential
ADD sequential /sequential
ADD flag.txt /sequential
ADD init.sh /bin
ADD sequential.xinetd /etc/xinetd.d/sequential

RUN groupadd -r sequential && useradd -r -g sequential sequential && \
    chown -R root:sequential /sequential && \
    chmod 750 /sequential/sequential.sh && \
    chmod 750 /sequential/sequential && \
    chmod 440 /sequential/flag.txt && \
    chmod 700 /bin/init.sh

RUN service xinetd restart

ENTRYPOINT [ "/bin/init.sh" ]

