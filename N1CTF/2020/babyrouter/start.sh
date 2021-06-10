#!/bin/sh
# Add your startup script

brctl addbr br0
ifconfig br0 10.10.10.10 up

service nginx start
nginx -t
nginx -s reload

PRO_NAME=qemu-arm
while true ; do
  NUM=`ps aux | grep ${PRO_NAME} | grep -v grep |wc -l`
  if [ "${NUM}" -lt "1" ];then
    echo "${PRO_NAME} was killed"
    ${PRO_NAME} -L /pwn /pwn/httpd >> /tmp/qemu.txt&
    rm /qemu_httpd*
    rm /tmp/core-qemu*
  fi
done


