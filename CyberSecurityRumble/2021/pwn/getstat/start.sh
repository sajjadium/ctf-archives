#!/bin/bash

socat TCP-LISTEN:3143,reuseaddr,fork,su=chall EXEC:"./getstat",stderr
