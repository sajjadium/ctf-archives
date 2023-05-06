FROM ubuntu:18.04
RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/ftp.sjtu.edu.cn/g" /etc/apt/sources.list
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y xinetd qemu-user
RUN useradd -u 8888 -m pwn
COPY flag2 /flag2
RUN chmod 400 /flag2
COPY readflag2 /readflag2
RUN chmod 4755 /readflag2
CMD ["/usr/sbin/xinetd", "-dontfork"]
