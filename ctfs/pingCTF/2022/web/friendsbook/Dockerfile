FROM node:18

RUN apt-get update && apt-get install -y npm

COPY ./src/ /app/

WORKDIR /app

RUN npm install
RUN npm install bcrypt
EXPOSE 3000

CMD ["npm", "run", "start"]
