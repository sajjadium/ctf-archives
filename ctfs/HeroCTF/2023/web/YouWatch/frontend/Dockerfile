FROM node:latest

ENV NEXT_PUBLIC_BACKEND=http://172.17.0.1:3000

WORKDIR /app
COPY package*.json ./
RUN npm i
COPY . .
RUN npm run build
RUN chmod -R 777 /app/.next/
EXPOSE 8000

USER 1000

CMD ["npm","run", "start"]