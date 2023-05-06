# sudo apt install qemu-user qemu-user-static
export mysql_pw=root
export mysql_user=root
export mysql_db=telnet
QEMU_SET_ENV=LD_LIBRARY_PATH=./lib QEMU_LD_PREFIX=./lib/ld-linux-armhf.so.3 qemu-arm ./telnet