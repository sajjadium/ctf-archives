FROM node:19-bullseye-slim

ARG configFile
RUN echo "${configFile}"

RUN mkdir -p /ctf/app
WORKDIR /ctf/app
COPY ./package.json ./
COPY ./package-lock.json ./
RUN npm install

COPY ./ ./
RUN echo "${configFile}" > ./config.json

EXPOSE 80

# run the app as a user who cannot modify the above files
USER node
CMD ["node", "index.js"]