#!/bin/bash

set -exuo pipefail

git clone https://github.com/terraforming-mars/terraforming-mars.git tfm
cd tfm
git checkout 03ffed02b
git apply ../challenge.patch
cp ../Dockerfile ../docker-compose.yml ../nginx.conf.template .
if [[ -f ../secret-env ]]; then
    cp ../secret-env secret-env
    cp ../htpasswd htpasswd
else
    touch secret-env
    touch htpasswd
fi
cat >> .dockerignore << EOF
secret-env
EOF
touch .env
