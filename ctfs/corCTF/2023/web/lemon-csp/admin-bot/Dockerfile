FROM node:18

ADD https://static.cor.team/corctf-2023/lemon-csp/chromium-browser-unstable_115.0.5790.114-1_amd64.deb /tmp/chrome.deb

RUN apt-get update && \
    apt-get install -y /tmp/chrome.deb && \
    rm -rf /tmp/chrome.deb /var/lib/apt/lists/*

WORKDIR /app

COPY ./package* .
RUN npm ci

COPY admin-bot.js .

USER node
CMD ["node", "admin-bot.js"]