#!/bin/bash

echo "Starting MySql..."
mysqld_safe &

while [[ $(/usr/sbin/service mysql status | grep "Uptime" | wc -l) -ne 1 ]]
do
    echo "Waiting for MySql to start..."
    sleep 1
done

echo "MySql started."

echo "Running setup.sql..."
mysql < /tmp/setup.sql

echo "Running web app..."
/tmp/app &

echo "Entering a shell now."
bash
