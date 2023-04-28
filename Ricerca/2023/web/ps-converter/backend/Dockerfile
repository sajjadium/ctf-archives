FROM golang:1.20.3-bullseye

RUN apt update -y &&\
    apt install -y ghostscript file

WORKDIR /backend
COPY index.html /backend/index.html
COPY main.go /backend/main.go
CMD go run main.go
EXPOSE 3000
