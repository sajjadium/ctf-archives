FROM node:14-slim

RUN apt update \
    && apt install -y libgtk-3-0 libdbus-glib-1-2 libxt6 \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /src/*.deb

ADD ./dumb-init_1.2.0_amd64 /usr/local/bin/dumb-init
RUN chmod +x /usr/local/bin/dumb-init

WORKDIR /app

ADD package.json /app/package.json
ADD package-lock.json /app/package-lock.json
RUN PUPPETEER_PRODUCT=firefox npm install

RUN groupadd -r pptruser && useradd -r -g pptruser -G audio,video pptruser \
    && mkdir -p /home/pptruser/Downloads \
    && chown -R pptruser:pptruser /home/pptruser \
    && chown -R pptruser:pptruser /app/node_modules

USER pptruser

ADD . /app

ENTRYPOINT ["dumb-init", "--"]
CMD ["npm", "start"]
