#!/bin/bash

while : 
do
	rm -rf /tmp/*
	socat TCP-LISTEN:15000,reuseaddr,fork EXEC:"./scripts/user_entry.sh"
done
