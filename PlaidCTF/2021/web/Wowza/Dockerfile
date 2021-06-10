FROM node:14

WORKDIR /problem

COPY package.json ./
COPY yarn.lock ./
COPY site-search/server/package.json ./site-search/server/package.json
COPY search-console/server/package.json ./search-console/server/package.json
COPY search-console/client/package.json ./search-console/client/package.json

RUN yarn install --frozen-lockfile

COPY . .