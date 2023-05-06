# Not important but just for your reference:
# - https://dlang.org/download.html (v2.098.0)
# - https://dlang.org/dmd-linux.html
chall: main.d
	dmd main.d -of=chall -O -release -inline -check=off
	mv chall ../distfiles
	cp main.d ../distfiles
	cp Makefile ../distfiles
