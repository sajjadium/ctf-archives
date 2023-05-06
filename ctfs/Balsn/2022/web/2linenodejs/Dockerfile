from node:18.8.0-alpine3.16
MAINTAINER ginoah

RUN apk add gcc musl-dev socat

COPY ./readflag.c /readflag.c
COPY flag /flag
RUN chmod 0400 /flag && chown root:root /flag
RUN chmod 0444 /readflag.c && gcc /readflag.c -o /readflag
RUN chown root:root /readflag && chmod 4555 /readflag

WORKDIR /app
COPY ./src/server.js ./
COPY ./src/index.js ./
COPY ./src/usage.js ./

USER nobody
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:'./server.js'"]
