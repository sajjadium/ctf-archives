FROM zenika/alpine-chrome:with-node

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD 1
ENV PUPPETEER_EXECUTABLE_PATH /usr/bin/chromium-browser
WORKDIR /usr/src/app

COPY --chown=chrome package-lock.json ./

RUN npm install puppeteer double-ended-queue
COPY --chown=chrome . ./

ENTRYPOINT ["tini", "--"]

CMD ["node", "/usr/src/app/bot.js"]
