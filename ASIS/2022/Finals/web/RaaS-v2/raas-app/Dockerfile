FROM node:latest

WORKDIR /app
COPY ./stuff/ /app
RUN npm install 
RUN chmod +x /app/index.js
RUN useradd -m app
USER app
ENV NODE_ENV=production
CMD ["/app/index.js"]
