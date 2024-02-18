FROM python:3.10

WORKDIR /app
RUN python3 -m pip install --no-cache-dir fastapi pydantic uvicorn
COPY app.py auth.py index.html flag.txt /app/
COPY static/ /app/static/

ENV PORT=8080
CMD ["uvicorn", "--log-level", "critical", "--host", "0.0.0.0", "--workers", "1", "app:app", "--port", "8080"]
