# Stage 1
FROM node as build-step
RUN mkdir -p /app
WORKDIR /app
COPY package.json /app
RUN npm install --force
COPY . /app
RUN npm run build --prod

# Stage 2
FROM nginx:1.21-alpine
COPY --from=build-step /app/dist/seoftw /usr/share/nginx/html
COPY ./nginx-custom.conf /etc/nginx/conf.d/default.conf
