FROM ubuntu:22.04

RUN apt-get update -y
RUN apt-get install -y xinetd

RUN useradd -mU ipc

COPY ./flag.txt /flag1.txt
COPY ./flag.txt /flag
COPY ./share/IPC /home/ipc/ipc
COPY ./xinetd /etc/xinetd.d/ipc

RUN chmod 750 /home/ipc /home/ipc/ipc
RUN chown -R root:ipc /home/ipc

CMD ["/usr/sbin/xinetd","-dontfork"]
