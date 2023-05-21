FROM alpine:3.17.0

# Init
RUN apk update && \
    apk add --no-cache python3 py3-pip nodejs npm chromium && \
# Create user
    adduser -D -u 1000 challenge && \
    echo "challenge:$(head -c 32 /dev/urandom | base64)" | chpasswd

# Copy chall data
ADD ./src /usr/app/
RUN chmod -R 777 /usr/app/;

# Setup bot
WORKDIR /usr/app/bot
RUN npm i

# Install python dependencies
RUN /usr/bin/python3 -m pip install -r /usr/app/requirements.txt

# Switch user
USER 1000:1000
WORKDIR /usr/app/

# Start
CMD ["/usr/bin/python3", "/usr/app/app.py"]
