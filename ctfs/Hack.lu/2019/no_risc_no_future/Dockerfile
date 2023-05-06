FROM i386/alpine

RUN apk add socat && addgroup -S chall && adduser -S chall -G chall

USER chall

COPY no_risc_no_future /chall/no_risc_no_future
COPY qemu-mipsel-static /chall/qemu-mipsel-static
COPY flag /chall/flag

# expose chall port
EXPOSE 1338

# run socat.sh
WORKDIR /chall
ENTRYPOINT ["/usr/bin/socat", "-t5", "-T60", "tcp-listen:1338,max-children=50,reuseaddr,fork", "exec:./qemu-mipsel-static no_risc_no_future,pty,raw,stderr,echo=0"]
