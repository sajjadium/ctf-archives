run: build
	./maltigriti

build:
	gcc maltigriti.c -g -o maltigriti

docker:
	docker build -t maltigriti .
	docker run -p 1024:1024 --rm -it maltigriti

solve:
	python3 solve.py

zip:
	zip -r pwn-maltigriti.zip maltigriti.c maltigriti solve.py Makefile Dockerfile README.md ynetd