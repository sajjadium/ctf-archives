FROM node:18-alpine

RUN mkdir /app
COPY src/ /app/src
COPY static/ /app/static
COPY *.json yarn.lock /app/
WORKDIR /app

RUN yarn install
RUN yarn build

COPY flag /flag
RUN mv /flag "/flag_$(head -n32 /dev/urandom | sha1sum | head -c32)"

USER 1000

EXPOSE 4001
CMD ["yarn", "start"]
