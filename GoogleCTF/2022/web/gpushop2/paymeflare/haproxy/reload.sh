#!/bin/bash
kill -SIGUSR2 `cat /var/run/haproxy.pid`

