all:
	gcc -shared -fPIC -fstack-protector-all -Wl,-z,now guardian.c pathlib.c util.c -o libguardian.so
clean:
	rm guardian
