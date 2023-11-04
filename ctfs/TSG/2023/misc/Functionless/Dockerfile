FROM node:20-slim

WORKDIR /app

RUN chown node:node ./

USER node

COPY --chown=node:node flag.txt ./
COPY --chown=node:node index.js ./

RUN mv flag.txt flag-$(md5sum flag.txt | awk '{ print $1 }').txt

CMD ["node", "index.js"]
