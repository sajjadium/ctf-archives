#!/bin/bash
set -e

M="$(netcat -l 4400)"

printf '{' >> /tmp/path

nl=$'\n'
if [[ ! "$M" =~ ^[VWXYZa-z$nl]+$ ]] ; then 
    exit 2
fi


if [[ $M != bracket* ]] ; then 
    exit 3
fi
M="{"${M:7}

P=$((145*$( echo -en "$M" | wc -l) + $(echo -en "$M" | wc -m ) ))

nnl=$'\nV'
M="${M//$nl/$nnl}"

if [[ $( echo -en "$M" | wc -l) -gt $(echo -en "$M" | head -n 1 | wc -c) ]] ; then 
    M=^$M
fi

echo -en "$M" | netcat -N 127.0.0.1 $P

