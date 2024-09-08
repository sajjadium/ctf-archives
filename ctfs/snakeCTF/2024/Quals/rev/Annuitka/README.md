Python is slow but simple. C is fast but complex.

What if you could have the best of both worlds?

To run the chall use this Dockerfile

FROM python:3.12.5-bullseye

RUN pip3 install --no-cache-dir cryptography
COPY chall /chall

ENTRYPOINT ["/chall"]
