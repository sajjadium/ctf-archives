FROM node:16.9.0

WORKDIR /amongst
ADD . .

# Need to yarn install in order to have esbuild
RUN yarn install --immutable

RUN yarn build
RUN yarn build-client
WORKDIR /amongst/packages/server
CMD ["yarn", "start"]
