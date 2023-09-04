FROM golang:1.20-alpine3.17

WORKDIR /app

COPY . ./

RUN go build -o app ./...

EXPOSE 8081

USER goodboy:goodboy

CMD ["./app"]
