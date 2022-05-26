# syntax=docker/dockerfile:1
FROM python:latest
ENV FLASK_APP=main.py
COPY --chown=root:root . ./microforum
WORKDIR ./microforum
RUN useradd -ms /bin/bash app
RUN chown -R app db/
RUN pip3 install -r requirements.txt
EXPOSE 8080
USER app
ENV FLAG='ptm{REDACTED}'
CMD ["python", "main.py", "--host=0.0.0.0"]
