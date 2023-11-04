FROM node:18-slim

WORKDIR /app

RUN groupadd -r pptruser && useradd -rm -g pptruser -G audio,video pptruser && chown -R pptruser /app && \
    apt-get update && apt-get install -y gnupg2 curl && \
    echo 'deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google.list && \
    curl 'https://dl-ssl.google.com/linux/linux_signing_key.pub' | apt-key add - && \
    apt-get update && apt-get install -y google-chrome-stable --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* && rm -rf /src/*.deb

USER pptruser

ENV PUPPETEER_SKIP_DOWNLOAD=true
ENV PUPPETEER_DISABLE_HEADLESS_WARNING=true

COPY --chown=pptruser package.json package-lock.json crawler.js /app/

RUN npm i

CMD ["node", "crawler.js"]
