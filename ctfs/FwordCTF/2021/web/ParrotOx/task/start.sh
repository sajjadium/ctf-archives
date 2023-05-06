#!/bin/bash
while ! exec 6<>/dev/tcp/db/3306; do
    echo "Trying to connect to MySQL..."
    sleep 10
done
exec java -jar /opt/app/stackoverctf.jar
