# Intermediate image - base for building and installing dependencies
FROM node:16.13.2-alpine3.15 AS install

# Install required tools
RUN apk add --no-cache --virtual .gyp git python3 make g++ \
  && ln -sf python3 /usr/bin/python

WORKDIR /usr/src/app

# Install dependencies first, to cache the image.
COPY ["package.json", "package-lock.json", "./"]

# Install dependencies
RUN npm ci


# Create image for application building
FROM install AS builder

# Copy sources
COPY [ "make_static_json.js", "package-lock.json", "tsconfig.json", "package.json", "webpack.config.js", "./"]
COPY "assets" "./assets/"
COPY "src" "./src/"

ENV SOURCE_VERSION=pctf

# Run building
RUN npm run build 


# Create image to prepare prod dependencies to be copied from
FROM install AS installProd

RUN npm ci --production --prefer-offline


# Node target
FROM nginx:1.21.6-alpine AS tfm-nginx

WORKDIR /usr/src/app

COPY htpasswd /etc/nginx/.htpasswd
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
COPY --from=builder /usr/src/app/assets ./assets
COPY --from=builder /usr/src/app/build ./build


# Target image
FROM node:16.13.2-alpine3.15 AS tfm-node

WORKDIR /usr/src/app

# Add user tfm
RUN adduser -S -D -h /usr/src/app tfm \
  && mkdir db \
  && chown -R tfm:nogroup .

USER tfm

# Copy required files.

COPY ["package.json", "package-lock.json", "./"]

COPY assets ./assets

# Copy dependencies from intermediate image
COPY --from=installProd /usr/src/app/node_modules ./node_modules

# Copy built app from intermediate image
COPY --from=builder /usr/src/app/build ./build

# Run command.

EXPOSE 8080

CMD npm run start
