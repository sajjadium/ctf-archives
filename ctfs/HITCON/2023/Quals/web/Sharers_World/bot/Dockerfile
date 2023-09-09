FROM node:20

WORKDIR /app

RUN apt-get update && apt-get install -y chromium

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

COPY ./ /app

RUN yarn add puppeteer express

CMD ["node", "index.js"]

