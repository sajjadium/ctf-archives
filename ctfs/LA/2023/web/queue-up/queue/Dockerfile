FROM node:19-bullseye-slim
ENV NODE_ENV=production

WORKDIR /app

COPY ["package.json", "package-lock.json", "./"]

RUN npm install --production

COPY queue.js /app
COPY dummy_data.csv /app
COPY views /app/views

COPY docker-entrypoint.sh /

RUN [ "chmod", "+x", "/docker-entrypoint.sh"]

CMD [ "bash", "/docker-entrypoint.sh"]