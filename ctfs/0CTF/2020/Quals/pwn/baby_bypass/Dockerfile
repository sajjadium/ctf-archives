FROM ubuntu:18.04
RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/ftp.sjtu.edu.cn/g" /etc/apt/sources.list
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y xinetd
RUN useradd -u 8888 -m pwn
COPY php /usr/local/bin/php
COPY pwnlib.so /usr/local/lib/php/extensions/no-debug-non-zts-20190902/pwnlib.so
COPY php.ini /usr/local/lib/php.ini
COPY flag /flag
RUN chmod 400 /flag
COPY readflag /readflag
RUN chmod 4755 /readflag
CMD ["/usr/sbin/xinetd", "-dontfork"]
