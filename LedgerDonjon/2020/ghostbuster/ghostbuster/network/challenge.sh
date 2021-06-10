#!/bin/bash

# For additional security, the challenge runs inside another container
# (hostname: ghostbuster, protocol: TCP, port: 8888) on the same machine.

exec nc -v ghostbuster 8888
