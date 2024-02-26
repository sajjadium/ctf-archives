FROM python:alpine
RUN pip3 install flask flask-caching uuid
RUN apk add sudo
COPY flag /
RUN chmod 700 /flag
RUN echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN adduser --disabled-password -u 1001 user
COPY --chown=user:user src /app
WORKDIR /app
EXPOSE 7000
USER user
RUN mkdir user_uploads
CMD ["python3","app.py"]
