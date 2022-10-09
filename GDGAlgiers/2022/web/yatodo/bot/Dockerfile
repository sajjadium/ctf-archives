FROM node:latest
RUN apt-get update \
    && apt-get install -y wget gnupg libxss1 ca-certificates procps\
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
      --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /bot
COPY . .
RUN yarn
RUN yarn cache clean

RUN chown -R root:node /bot/ 

USER node

CMD ["node", "bot.js"]