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
    python3 \
    py-pip \
    dumb-init \
    supervisor && \
pip install fastapi uvicorn aiofiles slowapi requests

# Tell Puppeteer to skip installing Chrome. We'll be using the installed package.
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Add user so we don't need --no-sandbox.
RUN addgroup -S inmate && adduser -S -g inmate inmate && \
mkdir -p /home/inmate/Downloads && \
chown -R inmate:inmate /home/inmate

WORKDIR /home/inmate
COPY apps ./
COPY supervisord.conf /etc/supervisord.conf

RUN chown -R inmate:inmate .
USER inmate

ENV NODE_ENV=production
RUN mkdir /tmp/boards && cd ./bot && npm install

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["supervisord"]
