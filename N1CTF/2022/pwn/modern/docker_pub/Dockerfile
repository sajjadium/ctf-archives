FROM ubuntu:22.04
# init env
RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.ustc.edu.cn/g" /etc/apt/sources.list;apt-get update && apt-get -y upgrade && apt-get install -y lib32z1 xinetd
# init /home/pwn
COPY pwnenv /home/pwn
# init pwnenv
RUN bash /home/pwn/init.sh && rm /home/pwn/init.sh
CMD ["/bin/sh", "/boot.sh"]