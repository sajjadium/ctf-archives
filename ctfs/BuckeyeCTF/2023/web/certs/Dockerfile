FROM oven/bun:1.0

WORKDIR /app

COPY package.json .
COPY bun.lockb .

RUN bun install

COPY private_key.pem .
COPY public_key.pem .
COPY buckeyectf-2023-logo.png .
COPY tsconfig.json .
COPY index.html .
COPY server.tsx .

ENV NODE_ENV production
CMD bun start
EXPOSE 3001
