FROM golang:1.19-alpine

RUN apk add socat

RUN addgroup -S casino && adduser -S casino -G casino
USER casino:casino
WORKDIR /home/casino

COPY ./go.mod .
COPY ./go.sum .
RUN go mod download

COPY . .
RUN mkdir ./build
RUN go build -o ./build/casino

CMD socat -T 30 -d -d TCP-LISTEN:31338,reuseaddr,fork EXEC:"./build/casino"
