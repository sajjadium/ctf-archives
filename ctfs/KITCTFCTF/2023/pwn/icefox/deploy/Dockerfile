# docker build -t icefox . && docker run -p 1337:1337 -t icefox
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -yq socat python3 python3-pip
RUN pip3 install --no-cache-dir pwntools

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf && echo "ctf:ctf" | chpasswd

COPY flag /flag
COPY catflag /catflag
RUN chmod u+s /catflag

RUN chmod 400 /flag

RUN mkdir /home/ctf/attempts
RUN chmod 777 /home/ctf/attempts

USER ctf
WORKDIR /home/ctf

COPY js /home/ctf/js
COPY wrapper.py /home/ctf/wrapper.py

EXPOSE 1337

ENTRYPOINT [ "socat", "tcp-listen:1337,reuseaddr", "EXEC:'/usr/bin/stdbuf -i0 -o0 -e0 python3 wrapper.py'" ]
