#!/bin/bash

pow(){
    difficulty=$1
    if [ $difficulty -gt 60 ]; then
        echo 'too hard'
        exit
    fi
    chalprefix=$(hexdump -n 8 -e '2/4 "%08x" 1 "\n"' /dev/urandom)
    echo "sha256($chalprefix+???) == $(printf '0%.0s' $(seq 0 $difficulty))($difficulty)..."
    printf "> "
    read -t 600 answer
    res=$(printf "$chalprefix$answer"|sha256sum|awk '{print $1}'|cut -c1-15|tr [a-f] [A-F])
    rshift=$((60-$difficulty))
    res=$(echo "obase=10; ibase=16; $res" | bc)
    if [ $(($res>>$rshift)) -ne 0 ]; then
        echo 'POW failed'
        exit
    else
        echo 'POW passed'
    fi
}

exec 2>/dev/null

#Please don't DoS, else I'll have to enable this :(
#pow 24

cd /home/guardian/challenge
exec timeout 1800 docker compose run --rm guardian
