# on host: docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
FROM arm64v8/ubuntu
ENV DEBIAN_FRONTEND=noninteractive 

#RUN apt update && apt install gcc gdb git -yy
#RUN git clone https://github.com/pwndbg/pwndbg && cd pwndbg && ./setup.sh
#RUN pip3 install pwn

RUN apt update && apt install socat gcc -yy
RUN mkdir /pwn

COPY cli /pwn/cli
#COPY cli.c /pwn/cli.c
#RUN gcc -D_FORTIFY_SOURCE=2 -fno-stack-protector -zexecstack -o /pwn/cli /pwn/cli.c && rm /pwn/cli.c
COPY flag.txt /pwn/flag.txt
COPY run.sh /pwn/run.sh

RUN groupadd ctf && \
    useradd -G ctf --home=/pwn pwn

# Helper/fixer for socat issues
COPY socat-sigpipe-fixup /pwn/socat-sigpipe-fixup
RUN chmod 111 /pwn/socat-sigpipe-fixup && \
    chmod 700 /pwn/run.sh


CMD "/pwn/run.sh"
