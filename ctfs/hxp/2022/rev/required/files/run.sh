#!/bin/bash

if [ "$(node required.js)" = "0xd19ee193b461fd8d1452e7659acb1f47dc3ed445c8eb4ff191b1abfa7969" ]; then
    echo ":)"
else
    echo ":("
fi