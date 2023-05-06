# expects wasmedge headers and libwasmedge_c.so to be in the same directory
chal: chal.c
	gcc chal.c -pie -O3 -lwasmedge_c -I./ -L./ -Wl,-rpath="./" -o chal
	strip chal
