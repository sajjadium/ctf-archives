FROM ubuntu AS app

RUN apt-get update && apt-get install -y gcc make

COPY . /app
RUN cd /app && make

WORKDIR /app

RUN useradd -m app
USER app

CMD ["./server"]