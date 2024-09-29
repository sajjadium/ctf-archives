FROM ubuntu@sha256:adbb90115a21969d2fe6fa7f9af4253e16d45f8d4c1e930182610c4731962658 AS app
RUN apt-get update && apt-get install -y g++ make wget

WORKDIR /app
COPY Makefile gpt2.cpp ./
RUN make
RUN rm Makefile gpt2.cpp
RUN wget https://huggingface.co/datasets/karpathy/llmc-starter-pack/resolve/main/gpt2_124M.bin
RUN wget https://huggingface.co/datasets/karpathy/llmc-starter-pack/resolve/main/gpt2_tokenizer.bin

FROM pwn.red/jail
COPY --from=app / /srv
ENV JAIL_TIME=90 JAIL_MEM=720M JAIL_CPU=500 JAIL_POW=7500
ENV JAIL_CONNS=4
# this chall usually eats up around 552 MB in memory, so we need to throttle hard with max conns and a ~10s proof of work
RUN mv /srv/app/gpt2 /srv/app/run
