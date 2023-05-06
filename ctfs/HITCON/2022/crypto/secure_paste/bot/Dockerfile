FROM mcr.microsoft.com/playwright:v1.27.1-focal

RUN mkdir /app
WORKDIR /app
COPY package.json yarn.lock .
RUN yarn

COPY . .
ENTRYPOINT ["yarn", "start"]
