FROM node:16.16.0 AS builder

WORKDIR /app
COPY ./package.json .
RUN yarn
COPY . .
RUN yarn build -m dev
RUN yarn cache clean

FROM nginx
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]