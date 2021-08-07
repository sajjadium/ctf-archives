FROM python:3.8.0-alpine
RUN apk add --no-cache redis
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
EXPOSE 50000-60000
COPY app.py app.py
ENTRYPOINT ["python", "app.py"]
