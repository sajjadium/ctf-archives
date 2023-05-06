FROM python:3

RUN pip install flask python-magic

COPY ./app /app
RUN mkdir -p /app/musics/

RUN useradd --no-create-home --home-dir /home/webapp --shell /bin/false webapp

RUN chown root:root /app/ && chmod -R 555 /app/
RUN chown webapp:webapp /app/musics/ && chmod 733 /app/musics/

RUN sed -i "s/___SECRET_KEY___/$(head -c 40 /dev/random | base32)/g" /app/app.py
RUN echo "hitcon{redacted}" > "/flag-$(head -c 32 /dev/random | sha1sum | cut -d ' ' -f 1 | tr -d '\n')"

USER webapp
WORKDIR /app/
EXPOSE 5000

ARG AUTO_DESTROY
ENV AUTO_DESTROY=$AUTO_DESTROY
CMD ["bash", "-c", "timeout $(($AUTO_DESTROY*60)) python app.py"]
