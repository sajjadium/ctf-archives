FROM node:16-slim

WORKDIR /app
COPY package.json ./
RUN npm install

COPY index.js ./
COPY static/ static/
COPY views/ views/

RUN mkdir uploads
RUN mkdir tmp

RUN chown -R node:node /app
RUN chmod -R 777 ./uploads
RUN chmod -R 777 ./tmp
USER node

EXPOSE 5000
CMD ["node", "index.js"]