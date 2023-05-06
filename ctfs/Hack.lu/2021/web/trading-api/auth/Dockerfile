FROM node:17-alpine

ENV NODE_ENV=production

WORKDIR /app/

ADD package.json yarn.lock /app/
RUN yarn install

ADD . /app/

USER 1000
ENV BIND_ADDR=0.0.0.0 PORT=3001
HEALTHCHECK --interval=1m --timeout=3s \
    CMD sh -c 'wget -qO /dev/null "http://localhost:${PORT}/health" || exit 1'

CMD ["node", "server.js"]
