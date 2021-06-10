FROM node:lts-alpine as build

WORKDIR /app

COPY ./app/package*.json ./

RUN npm install

COPY ./app .

RUN npm run build


FROM nginx

COPY --from=build /app/dist /app

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf