FROM node:20-slim

WORKDIR /app
RUN npm install -g pnpm

COPY ./types.ts ./

WORKDIR /app/client
COPY ./client/index.html ./client/package.json ./client/pnpm-lock.yaml \
    ./client/postcss.config.js ./client/tailwind.config.js ./client/tsconfig.json \
    ./client/tsconfig.node.json ./client/vite.config.ts ./
RUN pnpm install

COPY ./client/src/ ./src/
RUN pnpm build

WORKDIR /app/server
COPY ./server/tsconfig.json ./server/package.json ./server/pnpm-lock.yaml ./server/app.ts ./
RUN pnpm install

CMD pnpm start