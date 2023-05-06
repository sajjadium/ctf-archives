FROM node:18.12.1-bullseye-slim

WORKDIR /app

# Install dependencies
COPY ./package.json ./package-lock.json /app/
RUN PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
RUN npx playwright install --with-deps chromium

COPY . /app
COPY ./flag.txt /flag.txt

ENTRYPOINT ["node", "src/index.js"]
