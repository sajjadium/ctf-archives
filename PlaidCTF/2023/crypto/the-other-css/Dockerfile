FROM mwalbeck/python-poetry:1-3.11
RUN apt update && apt install -y socat wget bzip2
WORKDIR /install
RUN wget https://downloads.python.org/pypy/pypy3.9-v7.3.11-linux64.tar.bz2
RUN tar -xjf pypy3.9-v7.3.11-linux64.tar.bz2 \
	&& mv pypy3.9-v7.3.11-linux64 /opt/pypy3 \
	&& ln -s /opt/pypy3/bin/pypy3 /usr/local/bin/pypy3 \
	&& rm pypy3.9-v7.3.11-linux64.tar.bz2
WORKDIR /problem/css
COPY css/poetry.lock css/pyproject.toml ./
RUN poetry env use pypy3
RUN poetry install --no-dev --no-interaction --no-ansi
COPY css .
CMD ["socat", "TCP-LISTEN:1996,reuseaddr,fork", "EXEC:timeout 180 poetry run python -m css,pty,echo=0,raw,iexten=0"]

