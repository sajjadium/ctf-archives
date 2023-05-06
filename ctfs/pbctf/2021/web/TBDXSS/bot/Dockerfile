FROM node:15

RUN apt-get update \
    && apt-get install -y wget gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y libxss1 google-chrome-stable \
      --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /bot/
COPY bot.js /bot/

WORKDIR /bot/ 

RUN npm i puppeteer 
RUN npm i redis

RUN chown -R root:node /bot/ 

USER node

CMD ["node", "bot.js"]
