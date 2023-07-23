run:
	../run.sh ../initramfs.cpio exploit

debug:
	tmux split-window -h "sudo gdb ../vmlinux -x ../gdb.sh"
	$(MAKE) run
