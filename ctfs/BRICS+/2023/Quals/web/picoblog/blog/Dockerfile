FROM golang:1.21.1-alpine3.18 AS server-builder

WORKDIR /build

RUN echo "nobody:x:1337:1337:::" > etcpasswd
RUN echo "nobody::1337:nobody" > etcgroup
RUN mkdir secret

COPY go.* .
COPY cmd cmd
COPY internal internal
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o blog-web ./cmd/blog-web

FROM node:20.7.0-alpine3.18 AS front-builder

WORKDIR /build

COPY front/package.json front/package-lock.json .
RUN npm ci

COPY front .
RUN npm run build

FROM scratch

COPY --from=server-builder /build/etcpasswd /etc/passwd
COPY --from=server-builder /build/etcgroup /etc/group
COPY --from=server-builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=server-builder --chown=nobody:nobody /build/blog-web /blog-web
COPY --from=server-builder --chown=nobody:nobody --chmod=600 /build/secret /secret
COPY --from=front-builder --chown=nobody:nobody /build/build /front/build

WORKDIR /
USER nobody

CMD [ "/blog-web" ]
