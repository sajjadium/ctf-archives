FROM ubuntu:latest

RUN apt-get update && apt-get install -y xinetd libssl1.1 && rm -rf /var/lib/apt/lists/*

# ctf user
RUN useradd -m -s /bin/bash ctf

# challenge files
COPY babypwn /home/ctf/
COPY flag.txt /
COPY babypwn_svc /etc/xinetd.d/

CMD xinetd -dontfork
