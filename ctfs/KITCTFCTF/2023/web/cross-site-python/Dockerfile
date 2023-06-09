# docker build -t cross-site-python . && docker run -p 5000:5000 cross-site-python

FROM python:3.9-slim
WORKDIR /server

RUN apt-get update && apt-get -y install wget bzip2 \
&& rm -rf /var/lib/apt/lists/*

RUN mkdir static

RUN wget -O pyiodide.tar.bz2 https://github.com/pyodide/pyodide/releases/download/0.23.0/pyodide-0.23.0.tar.bz2
RUN tar -xf pyiodide.tar.bz2 -C ./static

RUN wget -O pyscript.css https://pyscript.net/latest/pyscript.css \
&& mv pyscript.css static/pyscript.css

COPY pyjail.js static/pyscript.js

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

RUN adduser --disabled-password --gecos "" user
USER user

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV URL=http://localhost

CMD ["flask", "run"]
