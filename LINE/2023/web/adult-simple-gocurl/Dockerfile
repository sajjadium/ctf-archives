FROM golang:1.19

ENV FLAG = "LINECTF{redacted}"
ENV GOCURL /usr/local/opt/gocurl
RUN mkdir -p "${GOCURL}"

RUN apt-get -qq update && \
  apt-get -qq -y upgrade && \
  apt-get -qq -y install htop net-tools vim curl 

ENV GO111MODULE=on \
    CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

COPY ./adult-simple-gocurl "${GOCURL}"
COPY start.sh "${GOCURL}/start.sh"

WORKDIR "${GOCURL}"
RUN go mod download
RUN go build -o main .

RUN chmod -R 705 "${GOCURL}"

RUN groupadd -g 1000 gocurl
RUN useradd -g gocurl -s /bin/bash gocurl

USER gocurl
EXPOSE 8080
WORKDIR "${GOCURL}"
ENTRYPOINT ["./start.sh"]
