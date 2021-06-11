FROM golang:1.15.7-alpine

WORKDIR /usr/local/go/src/
COPY ./main ./main
RUN cd main && go build -o gofs

FROM alpine:3.13.0
WORKDIR /task
COPY --from=0 /usr/local/go/src/main/gofs /task/gofs
COPY ./tmp /task/tmp

# We shall not be root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

CMD ["/task/gofs", "/task/tmp"]
