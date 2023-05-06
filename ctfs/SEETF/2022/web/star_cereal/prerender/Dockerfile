FROM node:14-alpine3.14

ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROME_PATH=/usr/lib/chromium/
ENV MEMORY_CACHE=0

# install chromium, tini and clear cache
RUN apk add --update-cache chromium tini \
 && rm -rf /var/cache/apk/* /tmp/*

WORKDIR "/home/node"

COPY ./package.json .
COPY ./server.js .

RUN chmod +r package.json server.js

# install npm packages
RUN npm install --no-package-lock

USER node

EXPOSE 3000

ENTRYPOINT ["tini", "--"]
CMD ["node", "server.js"]