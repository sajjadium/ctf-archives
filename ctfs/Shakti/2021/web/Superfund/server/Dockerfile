# docker build -t superfund:latest .
# docker run --name superfund --init -p 8080:8080 superfund:latest
FROM node:14.16-buster-slim

# Create app directory
WORKDIR /usr/src/app

# Install dependencies
COPY package*.json ./
RUN npm install --only=production

# Copy source
COPY server.js .
COPY public public

# Config and run
EXPOSE 8080
ENV NODE_ENV="production"
ENV FLAG="shaktictf{fake_flag}"
ENV ADMIN_SESSION="admin-session"
ENV ADMIN_PASSWORD="devpw"
ENV PORT="8080"
# ENV DEBUG="yup" # or "express:*"

USER node
CMD ["node", "server.js"]