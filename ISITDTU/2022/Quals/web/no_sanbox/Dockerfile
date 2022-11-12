FROM node:alpine

# Install packages
RUN apk --no-cache add supervisor g++ make python3

# Setup app
RUN mkdir -p /app

# Add application
WORKDIR /app
COPY challenge .

# Install node-js dependencies
RUN yarn

# Expose the port node-js is reachable on
EXPOSE 1337

# Setup supervisor
COPY config/supervisord.conf /etc/supervisord.conf

# Start the node-js application
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
