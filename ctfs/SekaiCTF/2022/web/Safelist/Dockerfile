FROM node:slim
WORKDIR /app
COPY package.json package-lock.json ./
COPY views ./views
COPY public ./public
RUN npm install
COPY app.js .
CMD ["node", "app.js"]