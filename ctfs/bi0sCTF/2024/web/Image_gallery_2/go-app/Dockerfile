
FROM golang:latest

WORKDIR /app

COPY src .

RUN go build -o main .
RUN mkdir /app/public
RUN useradd -ms /bin/bash user
RUN chown -R user:user /app/public
RUN chmod -R  +rx /app
USER user

EXPOSE 8080

CMD ["./main"]
