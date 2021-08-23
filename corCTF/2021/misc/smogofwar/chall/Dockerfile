FROM python:3.9.6-slim-buster

RUN apt-get update && apt-get install curl unzip -y && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN curl https://stockfishchess.org/files/stockfish_14_linux_x64_avx2.zip --output stockfish_14_linux_x64_avx2.zip

RUN unzip stockfish_14_linux_x64_avx2.zip

CMD ["sh", "start.sh"]
