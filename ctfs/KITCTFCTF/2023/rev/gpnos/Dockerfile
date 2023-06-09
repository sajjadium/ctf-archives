# docker build -t gpnos . && docker run -p 1337:1337 gpnos

from alpine/socat
RUN apk add qemu qemu-img qemu-system-i386 coreutils

COPY os-image.bin os-image.bin

RUN adduser --disabled-password --gecos "" user
RUN chmod 777 os-image.bin

USER user
EXPOSE 1337

ENTRYPOINT ["socat" ,"-v", "tcp-listen:1337,fork","EXEC:'/usr/bin/stdbuf -i0 -o0 -e0 qemu-system-i386 -nographic -fda os-image.bin'"]
