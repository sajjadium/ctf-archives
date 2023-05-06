FROM ubuntu:20.04
RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/ftp.sjtu.edu.cn/g" /etc/apt/sources.list && apt update && apt -y upgrade
RUN apt install -y xinetd
RUN useradd -u 10000 -m ctf

# build unicorn
RUN apt install -y python3 python3-pip wget
RUN wget https://github.com/unicorn-engine/unicorn/archive/refs/tags/1.0.3.tar.gz && tar xf 1.0.3.tar.gz
RUN cd /unicorn-1.0.3 && UNICORN_ARCHS="x86" ./make.sh && UNICORN_ARCHS="x86" ./make.sh install && pip install unicorn

COPY realflag readflag /
RUN chmod 400 /realflag && chmod 4755 /readflag

CMD ["/usr/sbin/xinetd", "-dontfork"]
