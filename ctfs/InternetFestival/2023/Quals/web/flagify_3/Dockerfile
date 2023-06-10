FROM node:18 as builder_bank

WORKDIR /app/bank
COPY bank/client ./
RUN npm install
RUN npm run build

FROM node:18 as builder_shop

WORKDIR /app/shop
COPY shop/client ./
RUN npm install
RUN npm run build


FROM nginx as final
WORKDIR /davy
COPY ./nginx/nginx.conf /etc/nginx/templates/default.conf.template
COPY --from=builder_bank /app/bank/build /usr/share/nginx/html/bank
COPY --from=builder_shop /app/shop/build /usr/share/nginx/html/shop
