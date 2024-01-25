FROM python:3.10

WORKDIR /app

RUN pip install flask requests

COPY index.py index.html ./

CMD ["python3", "index.py"]