all:
	gcc vuln.c -o vuln -fno-stack-protector -no-pie -lseccomp
	patchelf --set-interpreter ./ld-linux-aarch64.so.1 --replace-needed libc.so.6 ./libc.so.6 --replace-needed libseccomp.so.2 ./libseccomp.so.2 vuln
