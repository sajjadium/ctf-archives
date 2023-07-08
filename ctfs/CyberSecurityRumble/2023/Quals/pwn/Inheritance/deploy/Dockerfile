FROM ubuntu@sha256:7a57c69fe1e9d5b97c5fe649849e79f2cfc3bf11d10bbd5218b4eb61716aebe6

RUN apt update && apt install -y socat
RUN echo "8f7d59c6f95b0cf57a8db165033296dda91d1239  /lib/x86_64-linux-gnu/libc.so.6" | sha1sum -c

COPY ./flag.txt /flag.txt
RUN chmod 700 flag.txt

COPY ./child /child
COPY ./parent /parent
COPY ./harness /harness

RUN mkdir /home/game
RUN adduser --home /home/game game


RUN chmod 555 /child
RUN chmod 555 /parent
RUN chmod +s /parent
RUN chmod 555 /harness



CMD [ "socat", "tcp-l:1024,reuseaddr,fork", "EXEC:'/harness'" ]


#CMD ["su", "-c'socat tcp-l:1024,reuseaddr,fork EXEC:/harness'", "nobody"]