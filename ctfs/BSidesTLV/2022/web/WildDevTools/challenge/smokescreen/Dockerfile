FROM golang:1.18.3-alpine3.16

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app
ADD . .

RUN mkdir -p $GOPATH/src/github.com/stripe/smokescreen
RUN mv /app/smokescreen $GOPATH/src/github.com/stripe/smokescreen

RUN go install github.com/stripe/smokescreen@latest

RUN apk add --no-cache bash
RUN adduser --no-create-home --disabled-password -u 1337 user

USER user

CMD smokescreen