FROM wowza-base

RUN npx tsc --build site-search/server

CMD ["node", "site-search/server/index.js"]