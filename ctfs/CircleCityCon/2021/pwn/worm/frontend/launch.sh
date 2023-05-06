#!/bin/bash

set -eu

project=$(head -c16 /dev/urandom | xxd -p)
echo "cd /instance && docker-compose -p $project down" | at now + 6 min
cd /instance && docker-compose -p $project run app
