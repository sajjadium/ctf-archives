FROM python:3.9.1

WORKDIR /app

COPY ./ ./

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["python3", "server.py"]