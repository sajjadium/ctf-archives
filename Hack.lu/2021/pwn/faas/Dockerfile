
FROM ubuntu:21.04

RUN apt update
RUN apt install socat -y
RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

COPY NUCLEO_L152RE.bin libunicorn.so.1 run.sh faas /home/ctf/
COPY flag1.txt flag2.txt /home/ctf/

RUN chmod +x ./faas ./run.sh
RUN chown root:root /home/ctf/faas /home/ctf/run.sh
RUN chown root:root /home/ctf/flag1.txt /home/ctf/flag2.txt /home/ctf/libunicorn.so.1 /home/ctf/NUCLEO_L152RE.bin

USER ctf

CMD socat tcp-listen:4444,reuseaddr,fork exec:/home/ctf/run.sh,rawer,pty,echo=0
