#!/bin/bash

while true; do
    socat TCP-LISTEN:1222,reuseaddr,fork SYSTEM:'/app/target/release/main'
done
