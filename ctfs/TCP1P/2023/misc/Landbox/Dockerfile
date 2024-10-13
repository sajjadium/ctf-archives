FROM ubuntu:latest

RUN apt-get -y update
RUN apt-get -y install lua5.4 socat

RUN mkdir -p /ctf
WORKDIR /ctf
COPY main.lua .

COPY flag.txt /flag.txt
RUN chmod 744 /flag.txt
RUN chown root:root /flag.txt
RUN mv /flag.txt /flag-`md5sum /flag.txt | awk '{print $1}'`.txt

EXPOSE 1337
CMD socat TCP-LISTEN:1337,reuseaddr,fork 'EXEC:lua main.lua'

# docker build -t landbox .
# docker run --restart always --name landbox -p <port>:1337 -itd landbox