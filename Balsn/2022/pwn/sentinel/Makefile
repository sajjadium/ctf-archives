all:
	gcc -Wl,-z,now -fpie -fstack-protector-all -DDO_LOG sentinel.c -o sentinel
	strip sentinel

clean:
	rm sentinel
