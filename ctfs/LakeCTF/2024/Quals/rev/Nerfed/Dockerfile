FROM python:3.10.12@sha256:bac3a0e0d16125977e351c861e2f4b12ecafeaa6f72431dc970d0b9155103232

RUN pip install pyOpenSSL Pillow numpy 

COPY f.py .
COPY flag.npz .
COPY m.py .
COPY main.py .
COPY r.py .
COPY t.py .
COPY tz.npz .

# will need the -i flag
ENTRYPOINT ["python3", "main.py"]