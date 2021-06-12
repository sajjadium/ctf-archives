FROM alpine:edge

# https://github.com/puppeteer/puppeteer/blob/main/docs/troubleshooting.md#running-on-alpine

RUN apk add --no-cache \
    chromium \
    nss \
    freetype \
    freetype-dev \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    nodejs \
    npm \
    dumb-init

# Tell Puppeteer to skip installing Chrome. We'll be using the installed package.
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Add user so we don't need --no-sandbox.
RUN addgroup -S inmate && adduser -S -g inmate inmate && \
mkdir -p /home/inmate/Downloads && \
chown -R inmate:inmate /home/inmate

WORKDIR /home/inmate
COPY . ./

RUN chown -R inmate:inmate .
USER inmate

RUN cd ./app && \
mkdir -p /tmp/chrome && \
npm install

ENV NODE_ENV=production

WORKDIR /home/inmate/app
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["./start.sh"]
