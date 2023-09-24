FROM golang:1.21.1-alpine3.18 AS server-builder

WORKDIR /build

RUN echo "nobody:x:1337:1337:::" > etcpasswd
RUN echo "nobody::1337:nobody" > etcgroup
RUN mkdir genjidb

COPY go.mod go.sum .
RUN go mod download

COPY cmd cmd
COPY internal internal
COPY words words
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o dictionary-web ./cmd/dictionary-web

FROM node:20.5.0-alpine3.18 AS front-builder

WORKDIR /build

COPY front/package.json front/package-lock.json .
RUN npm ci

COPY front .
RUN npm run build

FROM scratch

COPY --from=server-builder /build/etcpasswd /etc/passwd
COPY --from=server-builder /build/etcgroup /etc/group
COPY --from=server-builder --chown=nobody:nobody /build/dictionary-web /dictionary-web
COPY --from=server-builder --chown=nobody:nobody --chmod=600 /build/genjidb /genjidb
COPY --from=front-builder --chown=nobody:nobody /build/dist /front/dist

WORKDIR /
USER nobody

CMD [ "/dictionary-web" ]