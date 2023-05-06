FROM node:17.0.1-slim
ENV NODE_ENV=production

RUN apt-get update \
    && apt-get install -yq wget gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -yq google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 x11vnc xvfb \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

ADD https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_x86_64 /usr/local/bin/dumb-init
RUN chmod +x /usr/local/bin/dumb-init

RUN groupadd -r pptruser && useradd -r -g pptruser -G audio,video pptruser \
    && mkdir -p /home/pptruser/Downloads \
    && mkdir -p /home/pptruser/.vnc \
    && x11vnc -storepasswd pass /home/pptruser/.vnc/passwd \
    && chmod 600 /home/pptruser/.vnc/passwd \
    && chown -R pptruser:pptruser /home/pptruser

WORKDIR /app

COPY ["package.json", "package-lock.json", "./"]

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

RUN npm install --production

COPY . .

USER pptruser

ENV DISPLAY=:99
ENTRYPOINT ["dumb-init", "--"]
CMD rm /tmp/.X99-lock 2>/dev/null; Xvfb -nolisten tcp -nolisten unix :99 & node index.js
