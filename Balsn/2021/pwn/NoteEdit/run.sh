#!/bin/bash

[ ! -d "./tmp" ] && mkdir ./tmp
CURDIR=`pwd`
NEWDIR=`mktemp -d tmp/XXXXXXXXXXXXXXXX`
cd $NEWDIR
export MallocMaxMagazines=1 # to make the challenge more deterministic (easier)
sandbox-exec -f $CURDIR/noteedit.sb $CURDIR/noteedit
cd $CURDIR
rm -rf $NEWDIR
