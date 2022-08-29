FROM node:alpine

# Create app directory
WORKDIR /usr/src/honksay

# env values
ENV PORT=9988
ENV FLAG="maple{fakefleg}"

RUN apk add --no-cache \
      chromium \
      nss \
      freetype \
      harfbuzz \
      ca-certificates \
      ttf-freefont \
      nodejs 

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Install rest of the packages
COPY package*.json ./
RUN npm install

# App src
COPY . .

# Expose port
EXPOSE 9988

# User
RUN addgroup -S ctf && adduser -S ctf -G ctf
USER ctf:ctf

# Start
CMD [ "node", "app.js"]
