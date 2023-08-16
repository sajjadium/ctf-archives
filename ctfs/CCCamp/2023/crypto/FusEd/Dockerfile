FROM python:3.10.5-slim-buster

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt update && apt install -y xinetd gcc && rm -rf /var/lib/apt/lists/*

RUN useradd --system --create-home ctf
WORKDIR /home/ctf

USER ctf

# Install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy challenge files
COPY --chown=ctf flag.txt ./
COPY main.py mcu.py ./
COPY python_svc /etc/xinetd.d/
RUN mkdir logs

EXPOSE 1024

CMD xinetd -dontfork
