FROM ubuntu:latest

# Set CWD to /app
WORKDIR /app

# Install packages
RUN apt-get update && apt-get install -y gcc curl patchelf net-tools ncat supervisor

# setup bianry with supervisor
RUN echo "[program:yeti]\ncommand=ncat -l -p 31337 -e /app/yeti\nautorestart=true" > /etc/supervisor/conf.d/yeti.conf

# Copy the current directory contents into the container at /app
ADD . /app

# Download pwninit from github
RUN curl https://github.com/io12/pwninit/releases/download/3.3.0/pwninit -o /bin/pwninit -L

# Set permissions
RUN chmod +x /bin/pwninit && chmod +x /app/compile.sh

# Compile the C program
RUN sed -i -e 's/\r$//' /app/compile.sh
RUN /bin/bash /app/compile.sh

# Make port 31337 available to the world outside this container
EXPOSE 31337

# Run the executable when the container launches using supervisor
CMD ["supervisord", "-n"]