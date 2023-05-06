FROM ubuntu:kinetic-20220922

RUN apt-get update
RUN apt-get install -y xinetd gdb
RUN apt-get clean

RUN useradd -m user

ADD --chown=user --chmod=755 share/wtfshell /home/user/wtfshell
ADD --chown=root --chmod=644 share/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
ADD --chown=root --chmod=755 share/ld-linux-x86-64.so.2 /lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
ADD --chown=user --chmod=755 share/run.sh /home/user/run.sh
ADD --chown=root --chmod=444 share/flag2 /flag2
ADD --chown=root --chmod=644 xinetd /etc/xinetd.d/wtfshell

USER root
WORKDIR /home/user

CMD ["/usr/sbin/xinetd", "-dontfork"]
