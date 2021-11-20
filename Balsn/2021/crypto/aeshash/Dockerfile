FROM ubuntu:20.04
MAINTAINER sasdf
WORKDIR /

RUN apt-get update && \
    apt-get install -y xinetd && \
    apt-get autoremove && apt-get autoclean && apt-get clean && \
    useradd -m aeshash

COPY ./src/chall /home/aeshash/
COPY ./src/run.sh /home/aeshash/
COPY ./xinetd.conf /etc/xinetd.d/chall
COPY ./flag /home/aeshash/

RUN chown -R root:root /home/aeshash && \
    chown -R root:root /etc/xinetd.d/chall && \
    chmod 755 /home/aeshash/chall && \
    chmod 755 /home/aeshash/run.sh && \
    find / -type d -perm /0002 -exec chmod o-w {} + 2>/dev/null ; \
    find / -type f -perm /0002 -exec chmod o-w {} + 2>/dev/null ; \
    echo 'Finish'

CMD ["/usr/sbin/xinetd", "-dontfork"]
