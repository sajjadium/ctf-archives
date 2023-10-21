#!/bin/bash

java -jar /root/SimpleAPI-1.0-SNAPSHOT.jar&
/opt/apache-activemq/bin/linux-x86-64/activemq console
# tail -f /dev/null


