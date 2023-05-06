#!/bin/bash

chmod -r flag3.exe
/usr/bin/socat -d -d TCP-LISTEN:9000,reuseaddr,fork EXEC:"timeout -sKILL 300 ./machine modules/init_module.img.sig",pty,stderr,setsid,sigint,sighup,echo=0,sane,raw,ignbrk=1
