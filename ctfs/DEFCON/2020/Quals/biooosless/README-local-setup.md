This challenge runs on Ubuntu 18.04, with qemu-system installed via apt-get (`qemu-system-x86 1:2.11+dfsg-1ubuntu7.23`).

You can test this on your ubuntu machine with: `python3 local-run.py shellcode.bin`

Or you can test this with the provided docker container:
- `docker build . -t biooosless-local -f Dockerfile-local-setup`
- `docker run -d --rm --name blocal biooosless-local`
- `docker cp your-shellcode.bin blocal:/`
- `docker exec -it blocal python3 /local-run.py /your-shellcode.bin`
