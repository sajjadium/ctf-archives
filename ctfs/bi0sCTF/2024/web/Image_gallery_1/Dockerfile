FROM node:lts

RUN apt update && \
    apt install -y curl gnupg2

RUN apt-get update && apt-get install gnupg wget -y && \
    wget --quiet --output-document=- https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /etc/apt/trusted.gpg.d/google-archive.gpg && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
    apt-get update && \
    apt-get install google-chrome-stable -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*
ENV NODE_ENV=production
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

WORKDIR /app
RUN mkdir /app/public


COPY src/package*.json .

RUN npm install

COPY src/ .

ENV FLAG=flag{hellow}

RUN useradd -ms /bin/bash user
RUN chown -R user:user /app/public
RUN chmod -R  +rx /app
USER user

CMD ["node", "app.js"]




