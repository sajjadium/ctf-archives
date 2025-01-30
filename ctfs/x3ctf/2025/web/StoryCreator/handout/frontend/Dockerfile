FROM node:22 AS builder 
WORKDIR /app
COPY package.json yarn.lock .yarnrc.yml /app/
COPY .yarn /app/.yarn
RUN yarn install --immutable
COPY . .
RUN yarn build
FROM nginx:alpine AS final 
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
