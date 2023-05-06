FROM node:18
WORKDIR /app
COPY package.json ./package.json
RUN npm i

COPY private.key .
COPY public.key .
COPY main.js ./main.js

CMD ["node", "main.js"]