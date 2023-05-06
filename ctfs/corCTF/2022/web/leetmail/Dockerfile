FROM node:18-bullseye-slim
WORKDIR /app
COPY code/package.json code/package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY code/ .
CMD ["node", "index.js"]
