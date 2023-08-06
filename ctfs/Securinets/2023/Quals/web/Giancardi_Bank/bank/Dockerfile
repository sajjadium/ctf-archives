# Build stage
FROM golang:1.20.6-alpine AS builder

RUN apk add --no-cache build-base

ENV USER webapp
ENV ACCOUNTANT_PASSWORD REDACTED

RUN adduser -D -g "" $USER 


WORKDIR /app

RUN chown -R root:root /app

COPY --chown=root:$USER go.mod go.sum ./
COPY --chown=root:$USER . .

RUN chmod 777 /app/log.txt
RUN chmod 777 /app/uploads

RUN go mod tidy
RUN go mod download

RUN GOOS=linux go build -o main cmd/main.go
RUN GOOS=linux go build -o setup cmd/setup.go


RUN mkdir db
RUN ./setup && rm setup

RUN chown -R $USER:$USER db/

RUN chmod 555 main

USER $USER

CMD ["./main"]
