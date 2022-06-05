FROM mcr.microsoft.com/dotnet/runtime:6.0-focal-amd64
WORKDIR /app

RUN useradd -m chall
RUN apt update
RUN apt install -y socat

COPY flag.txt .
COPY pointytail.dll .
COPY pointytail.runtimeconfig.json .

RUN chmod +r flag.txt
RUN chmod +r pointytail.dll
RUN chmod +r pointytail.runtimeconfig.json

USER chall

ENTRYPOINT socat tcp-l:1336,fork,reuseaddr exec:"dotnet pointytail.dll"