FROM node:16-buster AS build

WORKDIR /build
COPY server/package.json server/package-lock.json ./
RUN npm install

FROM node:16-buster-slim
COPY --from=krallin/ubuntu-tini /usr/bin/tini /tini
ENTRYPOINT ["/tini", "--"]

WORKDIR /app
COPY --from=build /build/node_modules ./node_modules
COPY server .
COPY flag.txt /

RUN mkdir views/uploads && chmod -R ugo+w views/uploads/

EXPOSE 3000

USER node

CMD ["node", "index.js"]
