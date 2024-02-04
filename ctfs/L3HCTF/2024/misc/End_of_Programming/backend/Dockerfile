FROM python:3.11-slim-bookworm
WORKDIR /app

COPY src/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY src /app

CMD ["gunicorn","-b","0.0.0.0","-w","4","main:app"]