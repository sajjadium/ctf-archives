docker build . -t asisctf2022_h.n.y
docker run \
	--rm \
	--name asisctf2022_h.n.y \
	-p 9000:9000 \
	-e FLAG=ASIS{test-flag} \
	asisctf2022_h.n.y
	# -d \
