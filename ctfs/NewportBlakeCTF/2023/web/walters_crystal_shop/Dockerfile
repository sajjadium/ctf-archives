FROM node:10.0.0-buster-slim
WORKDIR /usr/src/app
COPY ./package.json ./package-lock.json ./
RUN npm install
COPY . .
CMD ["npm", "start"]
