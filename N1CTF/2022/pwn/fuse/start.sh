#!/bin/bash

/spawner -w 200,28,35 # PoW
if [ $? -ne 0 ]; then
 	exit;
fi

temp_dir=$(mktemp -d)
chown root:root "${temp_dir}" || exit
chmod 775 "${temp_dir}" || exit

cp /flag ${temp_dir}/flag
chown fuse:fuse ${temp_dir}/flag
chmod 400 ${temp_dir}/flag

mkdir ${temp_dir}/work
chown root:root ${temp_dir}/work
chmod 775 ${temp_dir}/work

mkdir ${temp_dir}/usr
mkdir ${temp_dir}/etc

mount --bind -o ro /usr ${temp_dir}/usr
mount --bind -o ro /etc ${temp_dir}/etc
cd ${temp_dir}
ln -s ./usr/bin ./bin
ln -s ./usr/sbin ./sbin
ln -s ./usr/lib ./lib
ln -s ./usr/lib64 ./lib64
ln -s ./usr/lib32 ./lib32

cd /

mkdir -p ${temp_dir}/work/tmp/cfs
chown fuse:fuse ${temp_dir}/work/tmp/cfs

cp /cfs.disk ${temp_dir}/work/cfs.disk || exit
chown fuse:fuse "${temp_dir}/work/cfs.disk"

cp /spawner ${temp_dir}/spawner
chown root:root ${temp_dir}/spawner
chmod 500 ${temp_dir}/spawner || exit

cp /userinit.sh ${temp_dir}/init
chown root:root ${temp_dir}/init
chmod 500 ${temp_dir}/init || exit

# launch the world

/spawner -t 60 -c ${temp_dir} -p -n /init # timeout 60s , unshare(PID|MOUNT|NET|IPC)

# clean up

umount ${temp_dir}/usr ${temp_dir}/etc && rm -rf ${temp_dir} && echo "Bye"
