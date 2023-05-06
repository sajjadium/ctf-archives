FROM node:17-alpine as builder

RUN apk update && apk upgrade
WORKDIR /home/node/app

COPY package.json yarn.lock ./
RUN yarn install

COPY tsconfig.json  ./
COPY index.html  vite.config.ts ./
COPY src ./src
COPY includes ./includes
COPY img ./img

RUN yarn build

FROM nginx:alpine
COPY --from=builder /home/node/app/dist /usr/share/nginx/html