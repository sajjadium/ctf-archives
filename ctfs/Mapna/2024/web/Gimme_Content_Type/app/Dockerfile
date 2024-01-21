FROM node@sha256:0ded28778059262bd3c066b609186e5b6c89550a9362dce4309ad67c95af0d77

WORKDIR /app
COPY ./stuff/ /app
RUN npm ci 
RUN chmod +x /app/index.js
RUN useradd -m app
USER app
ENV NODE_ENV=production
CMD ["/app/index.js"]
