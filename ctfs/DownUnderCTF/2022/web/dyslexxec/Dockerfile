FROM python:3.9-alpine
RUN echo 'DUCTF{test_flag}:x:1001:1001::/tmp:/bin/false' >> /etc/passwd
WORKDIR /code
RUN mkdir uploads/
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD flask run --host=0.0.0.0 --port=1337
