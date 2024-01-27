FROM golang:1.21.5-bookworm

RUN apt update && apt install -y socat

RUN useradd -m -U adapt
USER adapt:adapt
WORKDIR /home/adapt

COPY ./go.mod .
COPY ./go.sum .
RUN go mod download

COPY . .
RUN go build -o adapt

CMD socat -T 30 TCP-LISTEN:31337,reuseaddr,fork EXEC:"./adapt"
