FROM node:16.20.2

WORKDIR /app
COPY static /app/static
COPY index.html /app/index.html
COPY app.js /app/app.js
COPY package.json /app/package.json

RUN npm install

RUN adduser ctf
USER ctf

EXPOSE 3000

CMD ["npm", "start"]
