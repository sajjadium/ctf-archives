FROM python:3.10.2-bullseye

WORKDIR /usr/src/app

COPY requirements.txt .
COPY flare.py .

RUN pip install --no-cache-dir -r requirements.txt

USER nobody
CMD ["python", "flare.py"]