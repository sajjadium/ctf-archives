FROM golang:latest
COPY app /app
WORKDIR /app
RUN go build
CMD ["/app/updater"]