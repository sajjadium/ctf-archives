FROM ubuntu:18.04
RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/ftp.sjtu.edu.cn/g" /etc/apt/sources.list
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y xinetd libreadline7
RUN useradd -u 8888 -m pwn
COPY mujs /usr/local/bin/mujs
COPY flag /flag
RUN chmod 400 /flag
COPY readflag /readflag
RUN chmod 4755 /readflag
CMD ["/usr/sbin/xinetd", "-dontfork"]
