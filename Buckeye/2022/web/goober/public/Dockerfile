FROM golang:1.19.2-bullseye

RUN apt-get update && \
    apt-get install -y libxml2 \
    libxml2-dev \
    libxml2-utils \
    libmagickwand-dev

COPY . /app/

# double copy, whatever
COPY ./policy.xml /etc/ImageMagick/policy.xml

WORKDIR /app

RUN go mod download
RUN go build -o ./server
CMD [ "/app/server" ]