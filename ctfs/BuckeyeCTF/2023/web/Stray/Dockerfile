FROM node:lts AS runtime
WORKDIR /app

RUN npm install -g pnpm

COPY package.json .
COPY pnpm-lock.yaml .

RUN pnpm install

COPY names names
COPY app.js .
COPY flag.txt .
COPY index.html .

EXPOSE 3000
ENV PORT=3000
ENV NODE_ENV=production
CMD pnpm start
