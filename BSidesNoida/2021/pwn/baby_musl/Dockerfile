#sudo docker build . -t test_chall
#sudo docker run -d -p 1024:1024 --rm -it test_chall

FROM ubuntu:20.04

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

COPY baby_musl .
COPY flag.txt .
COPY ynetd .

RUN chown -R root:root /home/ctf

RUN apt-get update && apt-get -y dist-upgrade && apt-get -y install musl

USER ctf
EXPOSE 1024

CMD ./ynetd -p 1024 ./baby_musl