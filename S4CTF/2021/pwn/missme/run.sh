#!/bin/bash
exec 2>/dev/null
./ld-2.28.so --library-path ./ ./missme
