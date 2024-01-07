# Build go app
FROM golang:1.20 AS golang
WORKDIR /src

COPY src/go.mod src/go.sum ./
COPY src/*.go ./

RUN go mod download
RUN CGO_ENABLED=0 GOOS=linux go build -o /tmp/app

# MySQL server
FROM ubuntu:22.04
WORKDIR /

RUN apt-get update
RUN apt-get install mysql-server -y

COPY setup.sql /tmp/
COPY entrypoint.sh /tmp/
COPY /src/web /web
COPY --from=golang /tmp/app /tmp/app

EXPOSE 10301

ENTRYPOINT ["/tmp/entrypoint.sh"]