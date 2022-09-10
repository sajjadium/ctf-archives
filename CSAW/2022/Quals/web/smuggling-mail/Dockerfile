FROM varnish:6.4.0

# Install packages and configure permissions
RUN apt-get update \
    && apt-get install -y hitch mailutils nodejs npm procps supervisor \
    && rm -rf /var/lib/apt/lists/* \
    && chown -R varnish:varnish /var/lib/varnish

# Create cert needed for HTTPS
WORKDIR /app/certs
RUN openssl req -newkey rsa:2048 -sha256 -nodes -x509 -days 365 \
    -subj "/CN=localhost/O=app/C=US" -keyout localhost.key -out localhost.crt \
    && cat localhost.key localhost.crt > localhost.pem

# Setup config files
COPY config/hitch.conf /etc/hitch/hitch.conf
COPY config/varnish.vcl /etc/varnish/varnish.vcl
COPY config/supervisord.conf /etc/supervisor/supervisord.conf
COPY config/entrypoint.sh /entrypoint.sh

# Setup app
WORKDIR /app
COPY challenge ./
RUN npm install --silent

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
