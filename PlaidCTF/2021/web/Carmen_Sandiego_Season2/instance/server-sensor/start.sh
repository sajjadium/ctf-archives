#! /bin/bash

# the iot hub has a weak networking stack
tc qdisc add dev eth0 root handle 1: prio priomap 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
tc qdisc add dev eth0 parent 1:2 handle 20: tbf rate 1mbit latency 50ms burst 1540
tc filter add dev eth0 parent 1:0 protocol ip u32 match ip sport 80 0xffff flowid 1:2

# init auth.txt
/goahead/goahead-gpl/build/linux-x64-default/bin/gopass --cipher md5 --file auth.txt --password $ADMIN_PASSWORD example.com admin dashboard

# set up flag file
echo $FLAG > /flag

# start up everything
touch /var/log/sensor.log
touch /var/log/goahead.log
python3 /sensor/server.py > /var/log/sensor.log 2>&1 &
goahead --log /var/log/goahead.log:2 /var/www/goahead &
tail -f /var/log/sensor.log -f /var/log/goahead.log
