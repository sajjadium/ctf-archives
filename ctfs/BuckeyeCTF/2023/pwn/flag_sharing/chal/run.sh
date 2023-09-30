#!/bin/sh

# Perfectly normal, nothing to see here
# 
# (note: this is for isolation between players so we
# can run more than one user on a box with minimal noise)
cp /srv/app/run /srv/app/run2
mv /srv/app/run2 /srv/app/run

# The normal redpwn/jail entrypoint
exec /jail/run
