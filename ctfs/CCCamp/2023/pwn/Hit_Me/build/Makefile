CC=clang
CFLAGS=-Wall -Wl,-z,relro -fstack-protector -fpie -pie -g
OUTDIR=.

hit_me: hit_me.c
	mkdir -p $(OUTDIR)
	$(CC) -o $(OUTDIR)/hit_me $(CFLAGS) hit_me.c
