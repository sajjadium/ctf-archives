#!/bin/bash

[ ! -d "./tmp" ] && mkdir ./tmp
CURDIR=`pwd`
NEWDIR=`mktemp -d ./tmp/XXXXXXXXXXXXXXXX`
cd $NEWDIR
sandbox-exec -f $CURDIR/machbookair.sb $CURDIR/machbookair
cd $CURDIR
rm -rf $NEWDIR
