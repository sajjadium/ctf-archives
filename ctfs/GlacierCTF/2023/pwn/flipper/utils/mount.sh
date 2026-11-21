#
# mount.sh
# mounts the SWEB-flat.vmdk image file to linux
#
mkdir /mnt/sweb
mkdir /mnt/sweb/part0
mkdir /mnt/sweb/part1
mkdir /mnt/sweb/part2
mkdir /mnt/sweb/part3
losetup /dev/loop4 ../sweb-bin/SWEB-flat.vmdk 
losetup -o 10321920 /dev/loop5 /dev/loop4
mount /dev/loop5 /mnt/sweb/part1

