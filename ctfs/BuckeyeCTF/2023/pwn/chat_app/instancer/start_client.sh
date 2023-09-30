#!/bin/bash

exec nsjail --config jail-client.cfg --macvlan_vs_ip $1 -- /client "$2:8000"