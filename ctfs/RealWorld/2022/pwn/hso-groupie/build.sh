#!/bin/bash -e

[ -f xpdf-4.03.tar.gz ] || wget https://dl.xpdfreader.com/xpdf-4.03.tar.gz
echo '0fe4274374c330feaadcebb7bd7700cb91203e153b26aa95952f02bf130be846  xpdf-4.03.tar.gz' | sha256sum -c || exit 2

docker build -t hsogroupie/pdftohtml . "$@"
