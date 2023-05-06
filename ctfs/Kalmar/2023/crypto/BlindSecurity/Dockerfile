# syntax=docker/dockerfile:1

FROM golang:1.20.1-alpine

WORKDIR /app

COPY go.mod ./
COPY go.sum ./
COPY flag.txt ./
RUN go mod download && apk --no-cache add netcat-openbsd

COPY *.go ./

RUN go build -o /server
EXPOSE 4343

CMD [ "/server" ]