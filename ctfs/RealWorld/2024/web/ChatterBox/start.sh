#!/bin/bash

/etc/init.d/postgresql start

sudo -u postgres psql -U postgres -f /init.sql

sleep 2

nohup java -jar /ChatterBox-0.0.1-SNAPSHOT.jar &

tail -f /etc/passwd

