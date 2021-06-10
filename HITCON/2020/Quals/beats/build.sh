#!/bin/bash
#

if [ $# -ne 4 ] ; then
    echo "Useage :./build.sh Problem Flag Port Binary"
else
    problem=$1
    flag=$2
    port=$3
    binary=$4
    find * -type f | xargs sed -i 's/beats/'$problem'/g'
    echo $flag > ./share/flag
    sed -i 's/problemport/'$port'/g' ./docker-compose.yml
    cp $binary ./share/
    chmod u+x ./share/$problem
    docker-compose up -d
fi
