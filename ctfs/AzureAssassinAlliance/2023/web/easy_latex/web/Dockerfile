FROM node:20.9.0-slim

ENV NODE_ENV=production
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

RUN apt-get update \
    && apt-get install -yq wget gnupg \
	&& wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -yq google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN openssl genrsa -out prv.key 2048 \
    && openssl rsa -pubout -in prv.key -out pub.key

RUN npm install

CMD ["node", "app.js"]