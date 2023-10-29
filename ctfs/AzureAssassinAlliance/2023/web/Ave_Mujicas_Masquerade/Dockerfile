# Use the official Node.js image as the base image
FROM node

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY ./src ./

COPY flag /flag

RUN mv /flag /flag-$(head -n 1000 /dev/random | md5sum | head -c 16)

# Install dependencies
RUN apt update
RUN npm ci
RUN apt install -y nmap python3-pip python3 wget curl

# Expose port 3333 inside the container
EXPOSE 3333

# Set the command to run the server
CMD ["npm", "start"]
