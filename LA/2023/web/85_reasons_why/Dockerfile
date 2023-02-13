FROM python:3.10

WORKDIR /app
COPY requirements.txt run.py /app/
ADD images /app/images/
ADD app /app/app/

RUN ls -la
RUN ls -la app

RUN chmod 444 /app/app/app.db

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=8080
CMD ["gunicorn", "-w", "1", "app:app"]
