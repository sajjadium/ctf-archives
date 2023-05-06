FROM node:18 AS pruner
WORKDIR /puzzled
RUN yarn global add turbo@1.2.16
COPY . .
RUN turbo prune --scope=@puzzled/server --docker

FROM node:18 as builder

WORKDIR /puzzled
COPY --from=pruner /puzzled/out/json .
COPY --from=pruner /puzzled/out/yarn.lock .
COPY .yarn .yarn
COPY .yarnrc.yml .yarnrc.yml
# Note: a direct `yarn install` is the best we can do due to limitations in turborepo, so it's possible that this
# actually doesn't use the versions in the lockfile.  However, everything we need _should_ be in the lockfile, and
# yarn _should_ prefer lockfile entries where they exist, so we'll probably be ok.
RUN yarn install
COPY --from=pruner /puzzled/out/full .
COPY tsconfig.*.json .
RUN yarn turbo run build --scope=@puzzled/server
CMD yarn workspace @puzzled/server start

FROM node:18

WORKDIR /puzzled
RUN yarn add reflect-metadata@0.1.13
COPY --from=builder /puzzled/packages/server/dist/index.mjs .
CMD node index.mjs
