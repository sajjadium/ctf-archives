FROM golang:1.17

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY static/ ./static/
COPY vulnerabilities.go ./
RUN go build vulnerabilities.go

EXPOSE 8080
USER 1234:1234
CMD ["./vulnerabilities"]
