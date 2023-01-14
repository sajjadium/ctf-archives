FROM python:3.9-slim
RUN pip3 install flask gunicorn
WORKDIR /app
COPY app.py .
ADD index.html .
ADD static ./static
EXPOSE 1337
CMD mount -t tmpfs none /tmp && python3 /app/app.py