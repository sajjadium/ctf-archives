FROM alpine:3.22

WORKDIR /app

RUN apk add --no-cache socat

COPY heapie2 ./

ARG FLAG
RUN echo "$FLAG" > /flag.txt

CMD ["socat", "tcp-listen:10447,fork", "exec:/app/heapie2,stderr"]
