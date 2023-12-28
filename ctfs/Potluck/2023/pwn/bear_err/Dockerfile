# docker build -t bear-err . && docker run --rm -it -p1024:1024 bear-err
# ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ctf@127.0.0.1 -p 1024

# build simple binary with the real flag:
FROM ubuntu:focal as builder
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y libssl-dev gcc make wget && apt-get clean
COPY chall /chall
RUN cd /chall && make
RUN openssl genrsa -out /chall/admin/key.pem 2048 && openssl rsa -in /chall/admin/key.pem -outform PEM -pubout -out /chall/admin/key.pub

# setup an SSH host with the flagcheck binary as execute-no-read
FROM ubuntu:focal
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3 python3-pip python3-requests curl dropbear rsync openssh-client openssl libssl-dev && apt-get clean # openssh-client provides scp
RUN pip install pwntools
ENV FLAG="fake{No_real_flag_here}"
COPY --from=builder /chall /chall
RUN echo -n $FLAG > /chall/admin/flag
RUN chmod -R 700 /chall/admin
RUN useradd -d /home/ctf/ -m -s /bin/bash ctf && passwd -d ctf
WORKDIR /home/ctf
CMD ["/bin/sh", "-c", "cd /chall && ./simple 10 10 8000 & 2>&1 1>/dev/null ; dropbear -FBREkwp 1024"]