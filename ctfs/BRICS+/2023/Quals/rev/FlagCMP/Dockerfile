FROM node:20.7.0-alpine3.18
ENV NODE_ENV production

WORKDIR /app

COPY --chown=node:node package.json package-lock.json .
RUN npm ci --only=production

COPY --chown=node:node views views
COPY --chown=node:node *.js impl.wasm .

USER node
CMD [ "node", "app.js" ]
