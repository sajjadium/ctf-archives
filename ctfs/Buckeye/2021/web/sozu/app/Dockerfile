FROM python:3

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app/
ENV PORT=8000
EXPOSE 8000

CMD gunicorn -k gthread server:app
