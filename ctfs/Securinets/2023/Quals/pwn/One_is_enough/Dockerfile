FROM ubuntu AS app

RUN useradd -p ctf ctf
RUN echo "ctf:ctf" | chpasswd

RUN mkdir /app
WORKDIR /app

COPY main .
COPY ynetd .
COPY run.sh .
COPY flag.txt .


USER ctf
CMD ./ynetd -p 5000 ./run.sh
