FROM ubuntu:18.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list 
RUN apt-get update && apt-get install -qy python3-dev


RUN useradd -m ctf

WORKDIR /home/ctf



COPY ./flag.txt /flag.txt
COPY ./junkav  /home/ctf
COPY ./run.sh /run.sh
COPY ./wrap.py /home/ctf
COPY ./libyara.so.4 /lib/x86_64-linux-gnu/
COPY ./rules /home/ctf/rules

RUN chmod +x /run.sh
RUN mkdir /home/ctf/check

RUN chown -R root:ctf /home/ctf && \
    chown -R root:ctf /home/ctf/check && \
    chmod -R 750 /home/ctf && \
    chmod 755 /lib/x86_64-linux-gnu/libyara.so.4


EXPOSE 9999

