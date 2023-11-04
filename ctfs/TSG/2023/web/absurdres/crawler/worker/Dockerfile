FROM node:20-slim

RUN apt-get update \
    && apt-get install -y wget gnupg2 libgconf-2-4 ca-certificates --no-install-recommends \
    && (wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg) \
    && sh -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-khmeros fonts-kacst fonts-freefont-ttf libxss1 --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /src/*.deb

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true

WORKDIR /app

ADD package.json /app/package.json
ADD package-lock.json /app/package-lock.json
RUN npm install

RUN groupadd -r pptruser && useradd -r -g pptruser -G audio,video pptruser \
    && mkdir -p /home/pptruser/Downloads \
    && chown -R pptruser:pptruser /home/pptruser \
    && chown -R pptruser:pptruser /app/node_modules

USER pptruser

ADD . /app

CMD ["npm", "start"]
