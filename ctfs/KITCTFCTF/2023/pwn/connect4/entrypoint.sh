#!/bin/bash
./game_server&
socat tcp-listen:1337,reuseaddr EXEC:'./client'
