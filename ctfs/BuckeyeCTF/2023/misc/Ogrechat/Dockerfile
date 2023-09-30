FROM node:lts-alpine AS runtime
WORKDIR /app

RUN apk add python3
RUN npm install -g pnpm

COPY package.json .
COPY pnpm-lock.yaml .

RUN pnpm install

COPY public public
COPY src src
COPY next.config.js .
COPY tailwind.config.ts .
COPY postcss.config.js .
COPY tsconfig.json .

RUN pnpm build

COPY flag flag
COPY entrypoint.sh entrypoint.sh

EXPOSE 8080
EXPOSE 3000
CMD ./entrypoint.sh
