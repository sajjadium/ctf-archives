FROM node:19-bullseye-slim
ENV NODE_ENV=production
ENV PORT=3500
ENV FLAG=lactf{testing}

WORKDIR /app

COPY ["package.json", "package-lock.json", "./"]

RUN npm install --production

COPY server.js /app

EXPOSE 3500

CMD [ "node", "server.js"]