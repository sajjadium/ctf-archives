FROM node:lts

RUN curl -L "https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose
WORKDIR /frontend/server
COPY package.json .
COPY yarn.lock .
RUN yarn install
COPY . .
RUN yarn build
CMD yarn start
