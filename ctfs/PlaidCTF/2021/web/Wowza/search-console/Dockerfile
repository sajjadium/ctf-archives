FROM wowza-base

RUN npx tsc --build search-console/server
RUN cd search-console/client/ && npx webpack build

CMD ["node", "search-console/server/index.js"]