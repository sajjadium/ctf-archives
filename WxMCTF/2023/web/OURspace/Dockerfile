FROM node:18
WORKDIR /ourspace
COPY package.json /ourspace
COPY . /ourspace
RUN npm run setup
CMD node .
