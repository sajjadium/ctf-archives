FROM golang:1.21.1 AS build-stage

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY *.go .

RUN CGO_ENABLED=0 GOOS=linux go build


FROM alpine AS release-stage
ENV GIN_MODE=release

WORKDIR /app

COPY views views
COPY notes notes
COPY shared shared
RUN chmod a+w notes shared
COPY --from=build-stage /app/app .

USER 404:404

ENTRYPOINT ["./app"]
