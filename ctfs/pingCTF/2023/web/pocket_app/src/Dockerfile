FROM alpine:3 as downloader

ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT

ENV BUILDX_ARCH="${TARGETOS:-linux}_${TARGETARCH:-amd64}${TARGETVARIANT}"

RUN wget https://github.com/pocketbase/pocketbase/releases/download/v0.19.4/pocketbase_0.19.4_${BUILDX_ARCH}.zip \
    && unzip pocketbase_0.19.4_${BUILDX_ARCH}.zip \
    && chmod +x /pocketbase

FROM alpine:3
RUN apk update && apk add ca-certificates && rm -rf /var/cache/apk/*
RUN apk add --update nodejs npm

EXPOSE 8090

COPY --from=downloader /pocketbase /usr/local/bin/pocketbase
COPY ./pb/pb_data /pb_data
COPY ./pb/pb_migrations /pb_migrations

COPY ./prepare /prepare
WORKDIR /prepare
RUN npm install
# The command below on the challenge deployment has been modified to include the real flag
RUN node /prepare/index.js ping{This-is-the-fake-flag}

WORKDIR /
RUN rm -rf /prepare

ENTRYPOINT ["/usr/local/bin/pocketbase", "serve", "--http=0.0.0.0:3000", "--dir=/pb_data", "--publicDir=/pb_public", "--migrationsDir=/pb_migrations"]
