#put your dockerfile contents here

FROM ubuntu:18.04 
# latest was giving glibc compatibility errors

RUN apt update && apt install socat gcc patchelf sudo -y


ENV USER easy-note
WORKDIR ../


COPY ./src/chal.c /chal.c

COPY ./dist/ld-2.27.so /
RUN mkdir -p /glibc/2.27/64/lib
RUN gcc /chal.c -o /chal
COPY ./dist/libc.so.6 /glibc/2.27/64/lib/

COPY ./flag.txt ./flag.txt


RUN chmod +x /chal
RUN patchelf --set-interpreter /ld-2.27.so /chal

EXPOSE 4400

CMD socat TCP-LISTEN:4400,reuseaddr,fork EXEC:"/chal"

