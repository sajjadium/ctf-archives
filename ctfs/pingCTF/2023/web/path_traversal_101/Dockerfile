FROM node:18-alpine

COPY ./src/ /app/

RUN apk update && apk upgrade
WORKDIR /app

RUN npm install

EXPOSE 3000

CMD ["npm", "run", "start"]
