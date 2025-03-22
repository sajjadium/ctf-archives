# Use an ARM-compatible base image
FROM arm32v7/gcc:latest

# Install additional tools (optional)
RUN apt-get update && apt-get install -y \
    build-essential \
    gdb \
    valgrind \
    python3-flask \
    python3-gunicorn 

COPY ./main.c /app/main.c
COPY secure_server.py /app/secure_server.py
COPY gunicorn_config.py /app/gunicorn.conf.py
EXPOSE 8080
RUN gcc -o /app/main /app/main.c
RUN rm /app/main.c
WORKDIR /app
CMD ["python3" ,"-m" , "gunicorn","--bind" , "0.0.0.0:8080","-w" , "4", "secure_server:app"]
# CMD ["/app/start.sh"]



# podman build -t  tick-tock --platform linux/arm/v7 .