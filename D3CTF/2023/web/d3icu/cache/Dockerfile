FROM golang:1.18.10-alpine as builder

ENV GOPROXY=https://goproxy.cn
# 
WORKDIR /build

ADD . .


RUN go build -o main

FROM alpine:latest

WORKDIR /app

COPY --from=builder /build/main .

CMD [ "/app/main" ]