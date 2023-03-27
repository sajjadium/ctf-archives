#!/bin/bash

printenv >> /etc/environment
crontab /usr/src/app/cron
cron -f