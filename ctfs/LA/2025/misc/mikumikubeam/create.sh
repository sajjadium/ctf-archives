#!/bin/sh
rm -rf build
mkdir build

flag="Pidgeon"

# below msg size and offset taken from docs
# miku actually randomized msg and offset owo
msgsize="50x40"
offset="+15+2"

# create the message gif
magick -gravity center -size $msgsize label:"$flag" build/message.gif
magick identify build/message.gif

# create steg image using imagemagick steg operator
magick composite build/message.gif mikumikubeam.png -stegano $offset build/mikumikusteg.png

cp build/mikumikusteg.png .
