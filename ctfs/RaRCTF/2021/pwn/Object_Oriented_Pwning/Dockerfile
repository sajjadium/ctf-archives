from ubuntu:18.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y socat cowsay
EXPOSE 1337
RUN useradd -m ctf

COPY cow.txt cow.txt
COPY pig.txt pig.txt
COPY flag.txt flag.txt
COPY oop /home/ctf/oop
USER ctf
CMD ["socat", "tcp-l:1337,reuseaddr,fork", "EXEC:/home/ctf/oop"]
