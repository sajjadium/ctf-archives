FROM python:3-alpine

WORKDIR /app
COPY flag /flag.txt
COPY src/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY src /app

EXPOSE 3000
CMD ["python", "main.py"]
