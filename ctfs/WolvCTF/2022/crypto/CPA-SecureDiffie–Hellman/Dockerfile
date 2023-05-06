FROM python:3.10.2-bullseye

WORKDIR /usr/src/app

COPY requirements.txt .
COPY key_exchange.py .
COPY flag.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["env", "FLASK_APP=key_exchange.py", "flask", "run", "--host=0.0.0.0", "--port=54321"]
