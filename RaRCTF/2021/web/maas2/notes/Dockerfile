FROM python:3.8.0-alpine
COPY flag.txt /flag.txt
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY app.py app.py
ENTRYPOINT ["python", "app.py"]
