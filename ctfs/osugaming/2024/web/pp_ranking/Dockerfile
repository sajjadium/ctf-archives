FROM node:20-buster-slim

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm i

COPY views ./views
COPY anticheat.js app.js ppcalc.js rankings.js ./

CMD ["node", "app.js"]