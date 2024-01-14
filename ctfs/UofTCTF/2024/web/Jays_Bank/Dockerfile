FROM node:20-bullseye-slim

RUN apt-get update && \
    apt-get install -y default-mysql-client netcat

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY index.js ./
COPY views ./views
COPY utils ./utils
COPY static ./static
COPY routes ./routes
COPY middleware ./middleware
COPY config/init.sql ./config/init.sql


EXPOSE 3000

CMD bash -c "echo Waiting for MySQL to start... && \
    while ! nc -z db 3306; do sleep 1; done; \
    echo MySQL started; \
    npm start"
