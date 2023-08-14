FROM golang:1.20.1 as build
WORKDIR /root
COPY . .
RUN go build -o bb_platform 

FROM debian:latest as prod
RUN apt update && apt install -y ca-certificates
COPY --from=build /root/bb_platform /bb_platform
RUN chmod +x /bb_platform
CMD ["/bb_platform"]
