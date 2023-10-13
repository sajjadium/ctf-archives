all: fortune-box

fortune-box: main.c banner.h
	$(CC) main.c -O2 -o fortune-box

banner.h: banner
	xxd -i banner > banner.h
