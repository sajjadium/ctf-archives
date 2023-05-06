#!/bin/bash
mkdir -p /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL
chown ctf /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL
cp sh /bin/sh
exec waitress-serve --call 'app:create_app'
