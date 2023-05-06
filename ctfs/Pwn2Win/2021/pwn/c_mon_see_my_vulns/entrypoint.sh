#!/bin/bash

# Secure entrypoint
chmod 600 /opt/entrypoint.sh

# start reverse proxy
nginx

# Start web service
apache2-foreground
