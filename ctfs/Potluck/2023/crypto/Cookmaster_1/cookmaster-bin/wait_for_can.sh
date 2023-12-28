#!/bin/sh

until [ -e /sys/class/net/vcan0 ]
do
  sleep 5
done

exit
