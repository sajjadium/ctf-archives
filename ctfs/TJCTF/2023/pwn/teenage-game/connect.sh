#!/bin/sh

# this script is just for fun, if you want to connect to the server and play the game in your terminal
OLD=$(stty -g)
stty -brkint -inpck -istrip -ixon -echo -icanon -iexten cs8

nc "$@"

stty "$OLD"
