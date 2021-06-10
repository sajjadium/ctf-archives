FROM ubuntu:20.04

RUN apt-get update -y && apt-get upgrade -y && apt-get install gcc -y
RUN apt-get install socat -y

COPY ./* /opt/
WORKDIR /opt/

RUN gcc tcache_king.c -o tcache_king -O2 -D\_FORTIFY\_SOURCE=2 -fstack-protector-all -Wl,-z,now,-z,relro -Wall -no-pie
RUN chmod 555 tcache_king
RUN chmod 444 flag.txt

CMD socat TCP-LISTEN:9124,reuseaddr,fork EXEC:"./tcache_king",su=nobody && fg
