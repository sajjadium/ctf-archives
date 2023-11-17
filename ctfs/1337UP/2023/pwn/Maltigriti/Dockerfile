FROM ubuntu:22.04

RUN apt-get update && apt-get install gcc -y

WORKDIR /chal

COPY maltigriti.c .
COPY ynetd .

RUN gcc -g -o maltigriti maltigriti.c

RUN chmod +x maltigriti ynetd

EXPOSE 1024
CMD ./ynetd -p "1024" /chal/maltigriti