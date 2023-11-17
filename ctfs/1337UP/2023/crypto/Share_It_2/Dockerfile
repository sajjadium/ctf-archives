FROM python:3.10

WORKDIR /opt/app

RUN pip install flask pycryptodome uuid waitress

COPY . /opt/app/

CMD ["python3", "./app.py"]