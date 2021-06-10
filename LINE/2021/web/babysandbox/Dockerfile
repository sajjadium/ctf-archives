FROM node:lts-alpine

ENV PORT 8000
ENV HOST 0.0.0.0
ENV FLAG LINECTF{this_is_fake_flag}

ADD ./app /app
WORKDIR /app
RUN chown -R node:node /app/views/sandbox

RUN npm install

EXPOSE 8000

USER node
CMD ["node", "app.js"]
