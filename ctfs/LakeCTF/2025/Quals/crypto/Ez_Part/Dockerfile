FROM python:3.10-slim
RUN pip install pycryptodome flask

COPY chall.py /app/
COPY default_vals.py /app/
CMD ["python3", "/app/chall.py"]
