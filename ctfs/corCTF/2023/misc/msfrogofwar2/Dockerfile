FROM python:3.9.17-bookworm

RUN apt-get update && apt-get install curl unzip -y && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN curl -L https://github.com/official-stockfish/Stockfish/releases/download/sf_16/stockfish-ubuntu-x86-64-avx2.tar --output stockfish-ubuntu-x86-64-avx2.tar

RUN tar xvf stockfish-ubuntu-x86-64-avx2.tar

CMD ["sh", "start.sh"]