FROM golang:1.19

ENV GO111MODULE=on \
    CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

RUN mkdir /app
RUN chmod -R 705 /app

WORKDIR /app

COPY server .
COPY static ./static
COPY templates ./templates

COPY module.wasm module.js ./static/

RUN go mod download
RUN go build -o main .

RUN groupadd -g 1000 wasmabism
RUN useradd -g wasmabism -s /bin/bash wasmabism

USER wasmabism

CMD ["./main"]
