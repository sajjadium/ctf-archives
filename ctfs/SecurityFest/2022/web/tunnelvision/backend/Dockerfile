FROM golang:1.17.2-alpine AS build

# Add required packages
RUN apk add --update git curl bash

# Install revel framework
RUN go get -u github.com/revel/revel
RUN go get -u github.com/revel/cmd/revel

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

ENV CGO_ENABLED 0

ADD . .

ENTRYPOINT revel run -m prod