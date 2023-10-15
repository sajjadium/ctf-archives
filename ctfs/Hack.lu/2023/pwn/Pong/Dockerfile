FROM alpine@sha256:7144f7bab3d4c2648d7e59409f15ec52a18006a128c733fcff20d3a4a54ba44a

RUN apk add --no-cache socat
RUN adduser -D ctf

COPY ./flag /flag
COPY ./pong /pong

EXPOSE 1440

USER ctf

ENTRYPOINT [ "socat", "tcp-l:1440,reuseaddr,fork", "exec:'/pong'" ]

