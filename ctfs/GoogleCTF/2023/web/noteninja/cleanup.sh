#!/usr/bin/bash
while true; do
  sleep 60m
  echo 'db.dropDatabase()' | mongo --shell $MONGO_URL
done