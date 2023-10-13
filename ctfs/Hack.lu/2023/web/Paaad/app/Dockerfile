FROM node:current-alpine


# install dependencies
RUN ["mkdir", "/install"]
ADD ["./package.json", "/install"]
WORKDIR /install
RUN npm install
RUN npm install -g nodemon
ENV NODE_PATH=/install/node_modules

WORKDIR /app

USER 1000

CMD npm run $NPM_RUN_SCRIPT