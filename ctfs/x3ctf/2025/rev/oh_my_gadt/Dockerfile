# Use the official Haskell image based on Ubuntu
FROM haskell:9.8.4
# Set the working directory
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install socat -y

# Copy the rest of your application code
COPY hs_src/. .

# Build the application
RUN stack build

# Specify the command to run your application
CMD ["/usr/bin/socat", "tcp-listen:4000,reuseaddr,fork", "exec:'stack exec ohmygadt'"]
