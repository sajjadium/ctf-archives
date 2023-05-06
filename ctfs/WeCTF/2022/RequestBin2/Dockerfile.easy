FROM golang:1.18

WORKDIR /app
RUN go mod init app
COPY views views
RUN mkdir logs
COPY main.go .
RUN go get github.com/kataras/iris/v12@master
RUN go build -o app

RUN echo "we{test}" > /flag

CMD ["./app"]