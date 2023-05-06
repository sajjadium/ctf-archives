FROM node:alpine

WORKDIR /ctf/app

RUN apk add --no-cache \
      chromium \
      nss \
      freetype \
      harfbuzz \
      ca-certificates \
      ttf-freefont \
      nodejs

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

COPY ./package.json ./
COPY ./package-lock.json ./
RUN npm install

COPY ./ ./

EXPOSE 8080

# User
RUN addgroup -S ctf && adduser -S ctf -G ctf
USER ctf:ctf

CMD ["/bin/sh", "start.sh"]
