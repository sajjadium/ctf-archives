#!/bin/sh
docker-compose up -d
bash -c "docker-compose exec mysql /bin/bash -c 'mysql -u root -pc546cfcba41c26715fc8c3caa7527832 < /db.sql'"
