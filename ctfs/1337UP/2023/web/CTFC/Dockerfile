FROM ubuntu@sha256:2adf22367284330af9f832ffefb717c78239f6251d9d0f58de50b86229ed1427
WORKDIR /app

# Install mongodb & other stuffs
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get install -y gnupg && \
    apt-get install -y supervisor && \
    apt-get install -y curl && \
    curl -fsSL https://pgp.mongodb.com/server-6.0.asc | gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor && \
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list && \
    apt-get update && \
    apt-get install -y mongodb-org && \
    mkdir -p /data/db

# Install Python,Flask & requirements
RUN apt-get install -y python3-pip
RUN pip3 install Flask
RUN pip3 install pymongo
RUN pip3 install passlib

# Copy stuffs
COPY . /app
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Setup flask app & create flag
EXPOSE 80
ENV FLASK_APP=/app/IntCTFC/app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_PORT=80
ENV FLASK_RUN_HOST=0.0.0.0
ENV CHALL_FLAG="1337UP{fl4G_h3RE}"
ENV SECRET_KEY="fake_secret_key"

# Run Mongodb & Flask
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]