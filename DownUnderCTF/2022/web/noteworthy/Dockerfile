FROM node:18.7-bullseye-slim AS run
WORKDIR /app

COPY . .
RUN yarn install --prod --frozen-lockfile && yarn cache clean

CMD ["yarn", "start"]
