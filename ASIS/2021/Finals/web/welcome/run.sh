#docker build . -t asisctf2021_welcome
docker run \
	-d \
	--rm \
	--name asisctf2021_welcome \
	--cap-add SYS_ADMIN \
	-p 8000:8000 \
	-e SITE_KEY=6LcX8MUdAAAAAEn66nxxrEzC0HhAPwBsBiGxQGAK \
	-e SECRET_KEY=REDACTED \
	-e SECRET_TOKEN=REDACTED \
	-e CHALL_DOMAIN=65.108.152.108 \
	-e FLAG=ASIS{fake-flag} \
	asisctf2021_welcome