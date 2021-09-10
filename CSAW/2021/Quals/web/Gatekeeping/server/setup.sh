#!/bin/bash

if [ ! -f /.dockerenv ]; then
    echo "This is supposed to be run in a docker env";
    exit
fi

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

cat > /etc/nginx/sites-enabled/default <<EOF
server {
    listen 80;

    underscores_in_headers on;

    location / {
        include proxy_params;

        # Nginx uses the WSGI protocol to transmit the request to gunicorn through the domain socket 
        # We do this so the network can't connect to gunicorn directly, only though nginx
        proxy_pass http://unix:/tmp/gunicorn.sock;
        proxy_pass_request_headers on;

        # INFO(brad)
        # Thought I would explain this to clear it up:
        # When we make a request, nginx forwards the request to gunicorn.
        # Gunicorn then reads the request and calculates the path (which is put into the WSGI variable `path_info`)
        #
        # We can prevent nginx from forwarding any request starting with "/admin/". If we do this 
        # there is no way for gunicorn to send flask a `path_info` which starts with "/admin/"
        # Thus any flask route starting with /admin/ should be safe :)
        location ^~ /admin/ {
            deny all;
        }
    }
}

EOF

