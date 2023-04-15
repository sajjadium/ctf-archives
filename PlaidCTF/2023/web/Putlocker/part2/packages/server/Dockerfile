FROM node:18 AS pruner
WORKDIR /davy
RUN yarn global add turbo@1.2.16
COPY . .
RUN turbo prune --scope=@davy/server --docker

FROM node:18 as builder

WORKDIR /davy
COPY --from=pruner /davy/out/json .
COPY --from=pruner /davy/out/yarn.lock .
COPY .yarn .yarn
COPY .yarnrc.yml .yarnrc.yml
# Note: a direct `yarn install` is the best we can do due to limitations in turborepo, so it's possible that this
# actually doesn't use the versions in the lockfile.  However, everything we need _should_ be in the lockfile, and
# yarn _should_ prefer lockfile entries where they exist, so we'll probably be ok.
RUN yarn install
COPY --from=pruner /davy/out/full .
COPY tsconfig.*.json .
RUN yarn turbo run build --scope=@davy/server
CMD yarn workspace @davy/server start

FROM node:18

WORKDIR /davy
RUN apt update && apt install -y chromium
RUN yarn add bcrypt@5.1.0 puppeteer@19.8.5
COPY --from=builder /davy/packages/server/dist/index.mjs .
RUN chown -R node:node /davy
USER node
ENV NODE_ENV production
CMD node index.mjs
