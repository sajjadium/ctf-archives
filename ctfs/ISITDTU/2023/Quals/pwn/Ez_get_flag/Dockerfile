FROM ubuntu:22.04

RUN apt-get update -y && apt-get install -y \
    lib32z1 xinetd \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf

WORKDIR /home/ctf

RUN cp -R /usr/lib* /home/ctf

RUN mkdir /home/ctf/warehouse && \
    mkdir /home/ctf/dev && \
    mknod /home/ctf/dev/null c 1 3 && \
    mknod /home/ctf/dev/zero c 1 5 && \
    mknod /home/ctf/dev/random c 1 8 && \
    mknod /home/ctf/dev/urandom c 1 9 && \
    chmod 666 /home/ctf/dev/*

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./start.sh /start.sh
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

RUN chmod +x /start.sh

COPY ./bin/ /home/ctf/
COPY ./warehouse /home/ctf/warehouse

RUN chown -R root:ctf /home/ctf && \
    chmod -R 755 /home/ctf && \
    chmod 744 /home/ctf/flag.txt && \
    chown -R root:ctf /home/ctf/warehouse && \
    chmod -R 755 /home/ctf/warehouse && \
    chmod 744 /home/ctf/warehouse/fake_file_name

CMD ["/start.sh"]

EXPOSE 3000