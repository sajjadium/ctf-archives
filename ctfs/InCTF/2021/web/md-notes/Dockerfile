FROM golang:alpine
RUN apk add build-base

WORKDIR /app

COPY deployment/go.mod .
COPY deployment/go.sum .
RUN go mod download

COPY deployment/src/. .

RUN go build -o /server

ENV ADMIN_BUCKET "REDACTED"
ENV FLAG "inctf{testFlag}"
ENV PORT ":8080"
ENV SECRET "REDACTED"
ENV VAL_A "REDACTED"
ENV VAL_B "REDACTED"

EXPOSE 8080

CMD [ "/server" ]
