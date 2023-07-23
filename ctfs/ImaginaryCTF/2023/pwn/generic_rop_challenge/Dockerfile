FROM ubuntu:focal

RUN /usr/sbin/useradd --no-create-home -u 1000 user
RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y socat

COPY libseccomp.so.2 /home/user/libseccomp.so.2
COPY ld-linux-aarch64.so.1 /home/user/ld-linux-aarch64.so.1
COPY libc.so.6 /home/user/libc.so.6
COPY flag.txt /home/user/flag.txt
COPY vuln /home/user/chal
RUN chmod 555 /home/user/chal

USER user
WORKDIR /home/user

CMD socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"/home/user/chal"

