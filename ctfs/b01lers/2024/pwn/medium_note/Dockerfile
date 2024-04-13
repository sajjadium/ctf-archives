#put your dockerfile contents here

FROM ubuntu:latest 

RUN apt-get update && apt-get install socat gcc patchelf sudo -y
# for debugging purposes
#RUN apt-get install python3 vim tmux python3-pip gdb -y
#RUN pip3 install pwntools 

ENV USER medium-note
WORKDIR ../


COPY ./src/chal.c /chal.c

COPY ./dist/ld-2.36.so /ld-2.36.so
# RUN mkdir -p /glibc/2.36/64/lib
# RUN gcc /chal.c -o /chal
COPY ./dist/chal /chal
COPY ./dist/libc-2.36.so.6 /libc.so.6

COPY ./flag.txt ./flag.txt


RUN chmod +x /chal
RUN patchelf --set-rpath . /chal

EXPOSE 4401

CMD socat TCP-LISTEN:4401,reuseaddr,fork EXEC:"/ld-2.36.so /chal"

