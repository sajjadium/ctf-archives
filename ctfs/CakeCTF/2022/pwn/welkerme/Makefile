exploit: exploit.c
	gcc exploit.c -o exploit -static

run: exploit
# clean up
	rm -rf vm/mount
	mkdir -p vm/mount
# copy exploit
	cd vm/mount; cpio -idv < ../rootfs.cpio
	cp exploit vm/mount/exploit
	cd vm/mount; find . -print0 \
		| cpio -o --null --format=newc --owner root > ../rootfs.cpio
# run qemu
	./run.sh

debug: exploit vm/mount
# clean up
	rm -rf vm/mount
	mkdir -p vm/mount
# copy exploit
	cd vm/mount; cpio -idv < ../debugfs.cpio
	cp exploit vm/mount/exploit
	cd vm/mount; find . -print0 \
		| cpio -o --null --format=newc --owner root > ../debugfs.cpio
# run qemu (debug port: 12345)
	./debug.sh
