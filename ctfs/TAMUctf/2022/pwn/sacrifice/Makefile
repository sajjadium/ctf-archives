run: docker
	docker run --restart=always --name sacrifice -p 7777:7777 sacrifice
stop:
	docker container rm -f sacrifice
docker:
	touch flag.txt
	docker build -t sacrifice .
dist:
	zip -r sacrifice.zip src static std-lol runners Makefile Dockerfile README.md Cargo.toml
