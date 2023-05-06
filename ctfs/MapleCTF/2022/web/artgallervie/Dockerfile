# Node docker image or ubuntu docker image and install node?
FROM node:alpine

# Create app directory
WORKDIR /usr/src/app

# env values
ENV PORT=8080
ENV FTP_PORT=8021

RUN apk add --no-cache \
      chromium \
      nss \
      freetype \
      harfbuzz \
      ca-certificates \
      ttf-freefont \
      nodejs \
      redis \
      libcurl \
      python3 \
      alpine-sdk \
      curl-dev

# App src
COPY . .

WORKDIR /usr/src/app/http
RUN npm install

WORKDIR /usr/src/app/ftp
RUN npm install

# Expose port
EXPOSE 8080

WORKDIR /
COPY run.sh .
RUN chmod +x run.sh
# User
RUN addgroup -S ctf && adduser -S ctf -G ctf
RUN chmod 555 usr/src/app
RUN chmod 777 usr/src/app/ftp/files
USER ctf:ctf


# Start
ENTRYPOINT [ "/run.sh"] 
