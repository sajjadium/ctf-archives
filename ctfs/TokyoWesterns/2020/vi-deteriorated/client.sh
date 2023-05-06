#!/bin/sh
stty -echo raw
nc localhost 4444
reset
