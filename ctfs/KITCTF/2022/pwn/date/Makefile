# yoinked from https://github.com/google/google-ctf/blob/master/2022/quals/pwn-d8/

.PHONY : all
all: challenge catflag

challenge: build.Dockerfile
	- docker rm tmp-d8-build-container 2>/dev/null
	docker build -t tmp-d8-build-image -f build.Dockerfile .
	docker run --name tmp-d8-build-container tmp-d8-build-image /bin/true
	docker cp tmp-d8-build-container:/build/v8/out/release/d8 .
	docker cp tmp-d8-build-container:/build/v8/out/release/snapshot_blob.bin .
	- docker rm tmp-d8-build-container 2>/dev/null

catflag: catflag.c
	gcc catflag.c -o catflag