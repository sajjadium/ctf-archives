FROM ubuntu:20.04 as ctf

RUN apt-get update && \
    apt-get install -y lib32z1 xinetd

RUN useradd -m ctf

WORKDIR /home/ctf

RUN cp -R /lib* /home/ctf && \
    mkdir /home/ctf/usr && \
    cp -R /usr/lib* /home/ctf/usr


RUN mkdir /home/ctf/dev && \
    mknod /home/ctf/dev/null c 1 3 && \
    mknod /home/ctf/dev/zero c 1 5 && \
    mknod /home/ctf/dev/random c 1 8 && \
    mknod /home/ctf/dev/urandom c 1 9 && \
    chmod 666 /home/ctf/dev/*

RUN mkdir /home/ctf/bin && \
    cp /bin/sh /home/ctf/bin && \
    cp /bin/ls /home/ctf/bin && \
    cp /bin/cat /home/ctf/bin && \
    cp /usr/bin/timeout /home/ctf/bin

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./start.sh /start.sh
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail


COPY ./chal/ /home/ctf/

RUN chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf && \
    chmod 740 /home/ctf/flag

RUN chmod +x /start.sh


# 
RUN chmod +x /home/ctf/run.sh
RUN chmod +x /home/ctf/ezROP
# 
CMD ["/bin/sh","/start.sh"]

EXPOSE 9999
