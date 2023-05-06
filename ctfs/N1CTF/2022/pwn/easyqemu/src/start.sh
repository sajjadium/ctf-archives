#! /bin/sh
for i in $(set | grep "_SERVICE_\|_PORT" | cut -f1 -d=); do unset $i; done

if [ -z "$(grep '^ctf:' /etc/passwd)" ]; then
  groupadd -r ctf && useradd -r -g ctf ctf
fi

if [ -d /ctf ]; then
  mv /ctf /home
fi

echo $FLAG > /home/ctf/flag
chown root:root /home/ctf/flag
chmod 444 /home/ctf/flag
export FLAG=114514

mkdir /home/ctf/lib
mkdir /home/ctf/lib64
mkdir /home/ctf/bin
mkdir -p /home/ctf/usr/lib
mkdir /home/ctf/dev
touch /home/ctf/dev/null
mount -o ro,bind /lib /home/ctf/lib
mount -o ro,bind /lib64 /home/ctf/lib64
mount -o ro,bind /bin /home/ctf/bin
mount -o ro,bind /usr/lib /home/ctf/usr/lib
mount -o bind /dev/null /home/ctf/dev/null
touch /var/log/xinted.log
xinetd -f /etc/xinetd.d/ctf && tail -f /var/log/xinted.log
