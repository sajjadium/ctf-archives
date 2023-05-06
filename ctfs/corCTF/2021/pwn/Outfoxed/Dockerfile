FROM python:slim
RUN apt-get update \
	&& apt-get install -y socat curl gzip \
	&& apt-get install -y --no-install-recommends \
	libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
	libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libgtk-3-0 \
	libasound2 libxshmfence1 libx11-xcb1 libdbus-glib-1-2 libxtst6 libxt6 && rm -rf /var/lib/apt/lists/*

COPY app/flag.txt /flag.txt
COPY app/reader /reader
RUN chmod 0640 /flag.txt && chmod 6755 /reader

RUN useradd -ms /bin/bash ctf

WORKDIR /app
RUN curl -fsS https://files.be.ax/outfoxed-7d11ebc85cf45e851977eda017da26ad71b225ecf28e3f2973fc1cbd09dd3286/outfoxed.tar.gz | tar x
COPY app/fox.py /app/flag.py

USER ctf
CMD  ["socat", "tcp-l:1337,reuseaddr,fork", "EXEC:/app/flag.py"]
