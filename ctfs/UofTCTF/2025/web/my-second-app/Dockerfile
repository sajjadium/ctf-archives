FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gcc make
RUN echo "uoftctf{fake_flag}" > /flag.txt && \
    chmod 400 /flag.txt && \
    chown root:root /flag.txt

RUN pip install flask

COPY ./readflag.c /readflag.c

RUN gcc /readflag.c -o /readflag
RUN rm /readflag.c
RUN chmod 4755 /readflag

WORKDIR /app
COPY ./src .

RUN groupadd -r flask && useradd -r -g flask flask

RUN chown -R flask:flask /app/
USER flask

EXPOSE 5000

# Run the application
CMD ["python", "guest_list.py"]