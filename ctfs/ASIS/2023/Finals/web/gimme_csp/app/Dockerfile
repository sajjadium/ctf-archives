FROM node@sha256:73a9c498369c6e6f864359979c8f4895f28323c07411605e6c870d696a0143fa

WORKDIR /app
COPY ./stuff/ /app
RUN npm ci 
RUN chmod +x /app/index.js
RUN useradd -m app
USER app
ENV NODE_ENV=production
CMD ["/app/index.js"]
