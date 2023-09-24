FROM golang:1.21-alpine

COPY waf /waf

WORKDIR /waf

RUN go build .

CMD ./waf
