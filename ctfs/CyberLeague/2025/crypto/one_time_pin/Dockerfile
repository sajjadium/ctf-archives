FROM alpine:latest

RUN apk add --no-cache python3
COPY app.py /app/app.py
COPY flag.txt /app/flag.txt

EXPOSE 10008
WORKDIR /app
CMD ["python3", "/app/app.py"]