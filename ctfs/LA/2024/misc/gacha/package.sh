#!/bin/sh
dd if=/dev/urandom ibs=1 count=128 > secret.key
rm -rf chall
mkdir -p chall
cp img/fiscl.png chall/

# add flag to uwu
magick img/uwu.png \
    -weight 50000 -fill red -pointsize 96 \
    -draw "text 50,540 '`cat flag.txt`'" \
    PNG24:flag.png

magick img/owo.png -encipher secret.key chall/owo.png
magick flag.png -encipher secret.key chall/uwu.png
rm flag.png

rm -f chall.zip
zip -9r chall.zip chall/
