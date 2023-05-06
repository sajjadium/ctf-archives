FROM debian:buster-20200803

RUN apt-get update -y && apt-get install xinetd -y

RUN mkdir -p /two

ADD two.sh /two
ADD two /two
ADD flag.txt /two
ADD init.sh /bin
ADD two.xinetd /etc/xinetd.d/two

RUN groupadd -r two && useradd -r -g two two && \
    chown -R root:two /two && \
    chmod 750 /two/two.sh && \
    chmod 750 /two/two && \
    chmod 440 /two/flag.txt && \
    chmod 700 /bin/init.sh

RUN service xinetd restart

ENTRYPOINT [ "/bin/init.sh" ]

