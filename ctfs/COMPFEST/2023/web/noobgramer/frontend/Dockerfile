FROM node:18-alpine AS build
WORKDIR /app
COPY . /app
RUN npm install
RUN npm run build
CMD ["npm", "run", "start"]