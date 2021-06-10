echo "welcome"
exec 2>/dev/null
exec timeout -k1 120 stdbuf -i0 -o0 -e0 \
qemu-system-x86_64 \
	-m 256M \
	-cpu qemu64,-smep,-smap \
	-kernel bzImage \
	-initrd root.cpio \
	-nographic \
	-append "root=/dev/ram rw console=ttyS0 oops=panic loglevel=2 panic=1 console=ttyS0" \
	-monitor /dev/null
