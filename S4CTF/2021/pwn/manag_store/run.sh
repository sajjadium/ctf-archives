#!/bin/bash

exec 2>/dev/null
./ld-2.31.so --library-path .  ./manga_store 
