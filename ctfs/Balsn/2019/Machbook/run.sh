#!/bin/bash

cd `dirname $0`
sandbox-exec -f ./machbook.sb ./machbook 2>/dev/null
