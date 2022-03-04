FROM node:16-buster-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . ./
ENTRYPOINT [ "./run-me.sh" ]
