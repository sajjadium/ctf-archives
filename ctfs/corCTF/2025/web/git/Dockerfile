FROM --platform=amd64 debian:trixie AS builder
WORKDIR /tmp
RUN apt-get update && apt-get install -y gcc
RUN echo '#include <stdio.h>\nint main() { puts("corctf{flag}"); }' > flag.c && \
	gcc -o flag flag.c && \
	chmod 111 flag
ADD https://fossil-scm.org/home/uv/fossil-linux-x64-202507091416.tar.gz fossil.tar.gz
RUN tar xf fossil.tar.gz

FROM --platform=amd64 debian:trixie
COPY --from=builder /tmp/flag /flag
COPY --from=builder /tmp/fossil /usr/bin/fossil
RUN useradd -ms /bin/bash ctf
USER ctf
WORKDIR /home/ctf
CMD USER=admin fossil init ctf.fossil && fossil server ctf.fossil