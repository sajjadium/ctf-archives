#!/bin/bash

docker-compose -p linectf_simple_blogger down
export ADMIN_USER=''
export ADMIN_PASS=''
docker-compose -p linectf_simple_blogger stop