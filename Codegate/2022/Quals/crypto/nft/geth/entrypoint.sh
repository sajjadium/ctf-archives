#!/bin/sh

if ! [ -d "/data/geth" ]; then
  geth init "/config/genesis.json" --datadir=/data
  cp /config/keystore/* /data/keystore/
fi

networkid=$(cat /config/genesis.json | jq '.config.chainId')

exec geth --datadir=/data \
--allow-insecure-unlock \
--networkid="$networkid" \
--nodiscover --mine \
--password="/config/password.txt" --unlock="0" \
--http --http.api=debug,eth,net,web3 --http.addr=0.0.0.0 --http.port=8545 --http.corsdomain='*' --http.vhosts='*'
