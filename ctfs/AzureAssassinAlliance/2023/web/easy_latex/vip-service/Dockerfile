FROM python:3.12.0-bookworm

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

ENV PORT=5000

CMD ["python3", "app.py"]