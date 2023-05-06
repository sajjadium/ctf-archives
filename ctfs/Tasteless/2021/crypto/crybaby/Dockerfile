FROM python:3.8-slim-buster
WORKDIR /app
RUN pip3 install cryptography
COPY crybaby.py flag ./
CMD [ "python3", "-u", "crybaby.py"]
