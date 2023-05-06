#!/bin/bash

sed -i 's/Connector port="8080"/Connector port="'"$TOMCAT_PORT"'"/' /usr/local/tomcat/conf/server.xml
sed -i 's/8005/-1/'  /usr/local/tomcat/conf/server.xml

exec "$@"