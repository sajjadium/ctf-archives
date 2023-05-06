FROM python:3.10
WORKDIR /opt/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD python setup.py && python server.py
