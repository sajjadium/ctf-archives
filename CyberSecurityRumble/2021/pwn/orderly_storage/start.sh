#!/bin/bash

socat TCP-LISTEN:3141,reuseaddr,fork,su=chall EXEC:"./orderly_storage",stderr
