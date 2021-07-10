FROM node:16 AS build
WORKDIR /app

COPY package.json yarn.lock .
RUN yarn install --frozen-lockfile && yarn cache clean

COPY public/ public/
COPY src/ src/

RUN yarn build

FROM nginx

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html
