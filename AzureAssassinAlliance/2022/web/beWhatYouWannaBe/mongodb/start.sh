#!/bin/bash
nohup mongod --bind_ip_all > /var/log/mongo.txt &
sleep 2
watch -n 1800 "mongo ctf --eval \"db.users.remove({});db.users.insertOne({username:'admin','password':'$password','isAdmin':true})\"" &>/dev/null &
tail -f /dev/null