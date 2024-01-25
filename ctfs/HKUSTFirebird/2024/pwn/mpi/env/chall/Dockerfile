FROM ubuntu:20.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
        tini xinetd libopenmpi-dev openmpi-bin\
        python3.9 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --no-create-home mpi && mkdir -p /home/mpi

COPY ./src /home/mpi/
COPY ./app.xinetd /etc/xinetd.d/app

RUN chown -R root:root /home && \
    find /home -type d -exec chmod 555 {} \; && \
    find /home -type f -exec chmod 444 {} \;

WORKDIR /home/mpi

RUN chmod +x /home/mpi/exec.sh
RUN chmod +x /home/mpi/mpi

EXPOSE 1337

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/usr/sbin/xinetd","-dontfork"]
