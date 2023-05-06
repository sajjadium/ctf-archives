#!/bin/bash

redis-server --save 20 1 --loglevel warning --requirepass Ogb8v3ufgpBf7r0dOLsll5OJN_CW3Vj5 --daemonize yes

flask run 
