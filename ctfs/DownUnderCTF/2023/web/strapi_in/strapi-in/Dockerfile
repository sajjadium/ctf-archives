FROM node:18-alpine

WORKDIR /opt/strapi-in
COPY ./package.json /opt/strapi-in/package.json
COPY ./package-lock.json /opt/strapi-in/package-lock.json

RUN npm config set fetch-retry-maxtimeout 600000 -g && npm install
ENV PATH /opt/node_modules/.bin:$PATH

COPY . .
RUN mv /opt/strapi-in/flag.txt /flag.txt
RUN chown -R node:node /opt/strapi-in/data
RUN chown -R node:node /opt/strapi-in/public/uploads
RUN chown node:node /opt/strapi-in/.env
RUN npm run build

USER node
CMD ["npm", "run", "start"]