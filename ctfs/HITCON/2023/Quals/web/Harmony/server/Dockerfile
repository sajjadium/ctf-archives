FROM node:18-bookworm-slim

RUN mkdir /app
COPY ./package.json ./yarn.lock /app
RUN yarn
COPY . /app
WORKDIR /app

RUN addgroup ctf && \
adduser --disabled-password --gecos "" --ingroup ctf ctf

USER ctf
CMD ["node", "app.js"]
