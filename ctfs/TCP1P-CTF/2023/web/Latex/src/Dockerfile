FROM golang:latest as build

EXPOSE 8080

WORKDIR /app
COPY go.mod .
COPY go.sum .
RUN go mod download
COPY . .
RUN CGO_ENABLED=1 go build -o latex

FROM ubuntu:latest

WORKDIR /app
RUN apt update -y
RUN apt install texlive-latex-base -y
COPY --from=build /app/latex .
COPY ./flag.txt /flag.txt
CMD [ "./latex" ]
