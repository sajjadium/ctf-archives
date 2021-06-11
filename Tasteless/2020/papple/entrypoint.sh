#!/bin/bash
python adjust_image.py || exit -1

Xvfb :0 -screen 0 1600x1200x16 &
x11vnc -forever -usepw -display :0 &
export DISPLAY=:0


sleep 1;
echo "Starting SheepShaver"
/usr/bin/SheepShaver
