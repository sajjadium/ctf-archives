#! /bin/sh

while :
do
    su -c "exec socat TCP-LISTEN:${LISTEN_PORT},forever,reuseaddr,fork EXEC:'/app/chall.py'" - user;
done
