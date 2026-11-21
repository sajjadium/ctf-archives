#
# umount.sh
# unmounts the SWEB-flat.vmdk image file from linux
#
umount /mnt/sweb/part1
losetup -d /dev/loop5
losetup -d /dev/loop4

