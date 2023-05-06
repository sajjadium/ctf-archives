# docker build -t maze . && docker run -p 1024:1024 --rm -it maze

FROM ubuntu:19.10

RUN apt-get update && apt-get install -y gdb # NOTE: installing gdb actually changes libc offsets ??
RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

COPY maze .
COPY flag .
COPY ynetd .

RUN chmod +x ./ynetd ./maze
USER ctf

CMD ./ynetd ./maze
