FROM ubuntu:20.04
WORKDIR /app

RUN apt update
RUN apt install -y --no-install-recommends xinetd

RUN useradd ctf

COPY stegosaurus-runner flag.txt ./
COPY xinetd /etc/xinetd.conf
RUN chmod 444 /app/flag.txt
EXPOSE 1337
ENTRYPOINT ["/usr/sbin/xinetd", "-dontfork"]

