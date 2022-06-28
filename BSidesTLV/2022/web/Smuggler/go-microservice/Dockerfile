FROM golang:1.17.7-alpine as build

WORKDIR /usr/src/app
COPY . .

RUN set -eux; \
    \
    go get; \
    go build


FROM alpine:3.16 as core

ARG USERNAME=app
WORKDIR /usr/src/app
COPY --from=build /usr/src/app/main .

RUN set -eux; \
    \
    apk add --no-cache socat; \
	\
	chmod +x /usr/src/app/main; \
    adduser --disabled-password --no-create-home --gecos ${USERNAME} ${USERNAME}

USER ${USERNAME}

EXPOSE 8080
CMD ["/usr/src/app/main"]
