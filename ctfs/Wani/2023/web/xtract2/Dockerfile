ARG GO_VERSION=1.19
ARG ALPINE_VERSION=3.17

# build-stage

FROM golang:${GO_VERSION}-alpine${ALPINE_VERSION} as build-stage

WORKDIR /app

COPY go.mod .
COPY go.sum .

RUN go mod download

COPY . .

RUN go build -o extract

# production-stage

FROM alpine:${ALPINE_VERSION} as production-stage

RUN addgroup appgroup && adduser --disabled-password --no-create-home appuser -G appgroup

WORKDIR /app

COPY --from=build-stage /app/extract .

COPY templates/ templates/

RUN chmod 771 ./extract

RUN chmod -R 444 ./templates

RUN echo "FAKE{FAKE_FLAG}" > /flag

RUN chmod 664 /flag

USER appuser

CMD ./extract
