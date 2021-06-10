FROM node:lts-alpine as base

ADD ./src /src
WORKDIR /src
COPY /src/package*.json /
EXPOSE 3000

FROM base as production
ENV NODE_ENV=production
ENV TARGET_HOST=private:5000
RUN npm install -g nodemon && npm install
RUN npm ci
COPY . /
CMD ["node", "bin/www"]

FROM base as dev
ENV NODE_ENV=development
ENV DEBUG=frontend:*
ENV TARGET_HOST=private:5000
RUN npm install -g nodemon && npm install
COPY . /
CMD ["nodemon", "bin/www"]

FROM base as local
ENV NODE_ENV=development
ENV DEBUG=frontend:*
ENV TARGET_HOST=localhost:5050
RUN npm install -g nodemon && npm install
COPY . /
CMD ["nodemon", "bin/www"]