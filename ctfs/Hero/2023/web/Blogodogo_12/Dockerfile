FROM alpine:3.17.0

RUN apk add --no-cache python3 py3-pip nodejs npm chromium && \
    adduser -D -u 1000 challenge

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

ENV PUPPETEER_SKIP_DOWNLOAD 1
RUN cd bot && npm install

USER 1000:1000

CMD ["python", "app.py"]
