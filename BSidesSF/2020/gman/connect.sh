#!/bin/bash

# Make sure no old settings are going to carry over
reset
clear

# Needed for proper art and colours
TERM=screen-256color

# stty to disable input buffering
stty -icanon
nc -v gman-ed6b851c.challenges.bsidessf.net 1337
#nc -v localhost 1337

# Reset the terminal settings to clear what we did
reset
