FROM ubuntu@sha256:b060fffe8e1561c9c3e6dea6db487b900100fc26830b9ea2ec966c151ab4c020

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt update && apt install -y socat
RUN ldd /bin/ls
RUN echo "8f7d59c6f95b0cf57a8db165033296dda91d1239  /lib/x86_64-linux-gnu/libc.so.6" | sha1sum -c


RUN useradd -u 1000 emxl

COPY ./flag.txt /flag.txt
RUN chown 1000:1000 /flag.txt
RUN chmod 700 /flag.txt

COPY ./main /main

RUN chmod 555 /main

CMD [ "socat", "tcp-l:1234,reuseaddr,fork", "EXEC:'/main'" ]