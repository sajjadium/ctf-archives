#! /bin/bash
pid=$(echo $$)
dirname=$(echo $RANDOM | md5sum | head -c 20)

mkdir /tmp/$dirname
cd /tmp/$dirname

cp -a /home/user/chall/* .

nohup /home/user/scripts/killscript.sh $pid $dirname &
echo "60 seconds, PWN!"
su -c "cd /tmp/$dirname && timeout 1m ./dirtyRAT" - rat

rm -rf /tmp/$dirname
