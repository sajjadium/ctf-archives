# docker build . -t asisctf2021_jsss
docker run \
	-d \
	--rm \
	--name asisctf2021_jsss \
	-p 8000:8000 \
	-e SECRET_MESSAGE=SECRET \
	asisctf2021_jsss
