FROM golang:1.21.2-alpine3.18 as builder

WORKDIR /app
COPY go.mod go.sum .
RUN go mod download && go mod verify

COPY ./*.go .
RUN go build -v ./...

FROM alpine:3.18

WORKDIR /app
COPY --from=builder /app/countdown-manager .
COPY ./static ./static

CMD ["/app/countdown-manager"]
