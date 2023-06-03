FROM node:18-alpine

COPY ./src/ /app/

RUN apk update && apk upgrade
RUN apk add chromium 

WORKDIR /app
RUN echo "justCTF{This_is_a_fake_flag}" > flag.txt

RUN npm install
EXPOSE 3000
CMD ["npm", "run", "start"]
