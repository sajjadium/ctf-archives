FROM ubuntu:22.04

RUN apt update
RUN apt install socat -y
RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf

RUN echo "ctf:ctf" | chpasswd

RUN apt install libc6-dbgsym -y

EXPOSE 4444

WORKDIR /home/ctf

ADD rustymix /home/ctf/
COPY flag.txt /home/ctf/

RUN chmod 555 /home/ctf/rustymix
RUN chown root:root /home/ctf/rustymix
RUN chown root:ctf /home/ctf/flag.txt
RUN chmod 440 /home/ctf/flag.txt

USER ctf

CMD socat tcp-listen:4444,reuseaddr,fork exec:/home/ctf/rustymix,rawer,pty,echo=0
