FROM node:19-alpine3.16 AS common

WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci

FROM common AS build

COPY vite.config.ts tsconfig.json ./
COPY src ./src
COPY public ./public
RUN npm run build

FROM common

COPY context/docker-entrypoint.sh /usr/local/bin
COPY --from=build /work/dist ./dist

CMD [ "npm", "start" ]
