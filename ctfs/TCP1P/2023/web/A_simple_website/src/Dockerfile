# Use the official Node.js image as the base image
FROM node:18

# Install PNPM
RUN npm uninstall -g yarn pnpm
RUN npm install -g corepack

#RUN mkdir /.cache && chmod -R 777 node_modules/.cache

# Set the working directory in the container
WORKDIR /app

# Clone the Nuxt.js repository and switch to the desired release
RUN git clone https://github.com/nuxt/framework.git /app && \
    cd /app && \
    git checkout v3.0.0-rc.12

# Copy the test.txt file from the build context into the container
COPY flag.txt /

# Copy app.vue into container
COPY app.vue /app/playground/

# Install project dependencies using pnpm
RUN pnpm install
RUN pnpm build:stub

# Add new user named ctf and add permission for corepace
RUN useradd -ms /bin/bash ctf

RUN mkdir /home/ctf/.cache && chmod -R 777 /home/ctf/.cache && chmod -R 777 /app

# Change to user ctf
USER ctf

# Expose the port that Nuxt.js will run on
EXPOSE 3000

# Start the Nuxt.js development server
CMD ["pnpm", "run", "dev", "--host", "0.0.0.0"]
