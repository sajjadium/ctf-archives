FROM python:alpine3.8
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY static static
COPY templates templates
EXPOSE 5000
COPY app.py app.py
ENTRYPOINT ["python", "app.py"]
