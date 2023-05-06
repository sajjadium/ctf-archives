#!/bin/bash
echo 1 > /proc/sys/fs/suid_dumpable
echo 0 > /proc/sys/kernel/yama/ptrace_scope
mkdir ./no-write
chown root ./no-write
chmod 000 ./no-write
docker-compose build && docker-compose up --force-recreate --remove-orphans
