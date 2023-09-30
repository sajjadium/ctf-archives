FROM oven/bun:1.0

RUN apt-get update
RUN apt-get install -y chromium

WORKDIR /app

COPY package.json package.json
COPY bun.lockb bun.lockb

RUN bun install

COPY default.md default.md
COPY styles.css styles.css
COPY tsconfig.json tsconfig.json
COPY server.tsx server.tsx

ENV NODE_ENV production
CMD bun start
EXPOSE 3001
