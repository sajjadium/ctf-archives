FROM node:latest

WORKDIR /app
COPY package*.json ./
RUN npm i
COPY . .
RUN chmod -R 777 /app/videos/ && apt update && apt install chromium -y && chmod +x run.sh
EXPOSE 3000

USER 1000

CMD ["bash","/app/run.sh"]