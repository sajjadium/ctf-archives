# docker build -t notian . && docker run -p 8081:8081 notian

FROM nimlang/nim:alpine as builder

COPY . /build
WORKDIR /build

RUN nim c -d:release main.nim

FROM alpine:3.17

RUN apk add --no-cache sqlite-libs
RUN mkdir /data

COPY --from=builder /build/main /notian
COPY --from=builder /build/notes.sqlite /data/notes.sqlite

RUN chown -R 65534:65534 /data

USER 65534
EXPOSE 8081

ENTRYPOINT ["/notian"]
