FROM python 

FROM python:3.10

WORKDIR /usr/src/app

RUN pip install --no-cache-dir pwntools
COPY . .

ENTRYPOINT [ "python3", "bot.py" ]
