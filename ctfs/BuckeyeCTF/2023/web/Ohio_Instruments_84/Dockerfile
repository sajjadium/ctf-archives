FROM gnuoctave/octave:8.3.0

RUN useradd -m ctf
WORKDIR /home/ctf

RUN curl -fsSL https://bun.sh/install | bash && cp /root/.bun/bin/bun /usr/bin

COPY flag.txt index.ts index.html ./
RUN chmod 444 index.ts index.html flag.txt

USER ctf

CMD ["bun", "index.ts"]