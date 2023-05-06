FROM python:3.6-slim
RUN apt-get update && \
    apt-get install libgomp1 && \
    rm -rf /var/lib/apt/lists/*
RUN pip install \
    paddle-serving-server==0.9.0 \
    paddle-serving-client==0.9.0 \
    paddle-serving-app==0.9.0 \
    paddlepaddle==2.3.0
WORKDIR /usr/local/lib/python3.6/site-packages/paddle_serving_server/env_check/simple_web_service
RUN cp config_cpu.yml config.yml
RUN echo "rwctf{this is flag}" > /flag
CMD ["python", "web_service.py"]
