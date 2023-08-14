FROM node:16-alpine as build
COPY ./react /app
WORKDIR /app
RUN npm ci --cache .npm
COPY . ./ 
RUN npm run build 

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80