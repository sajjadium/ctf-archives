#docker build . -t asisctf2021_classic
docker run \
	-d \
	--rm \
	--name asisctf2021_classic \
	--cap-add SYS_ADMIN \
	-p 8000:8000 \
	-e FLAG=ASIS{test-flag} \
	asisctf2021_classic