#!/bin/sh

NSJAIL_DIR=/sys/fs/cgroup/memory/NSJAIL/

if [ ! -d "$NSJAIL_DIR" ]; then
    mkdir $NSJAIL_DIR
fi
nsjail -Mo --user 9999 --group 9999 -R /bin/ -R /lib/ -R /lib64/ -R /usr/ -R /sbin/ -T /tmp/ -R /tmp/$1/bin/Release/ --quiet --time_limit 100 --cgroup_mem_max 100000000 -- /tmp/$1/bin/Release/net5.0/proj_template
