FROM golang:1.21-alpine

COPY app /app

WORKDIR /app

RUN go build .

CMD ./chadgpt
