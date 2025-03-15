#!/bin/bash

while [ true ]; do
	socat -dd TCP4-LISTEN:9000,fork,reuseaddr EXEC:'/chal',pty,echo=0,rawer,iexten=0
done;
