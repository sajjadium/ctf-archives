FROM python:alpine3.7
RUN pip3 install --upgrade pip

RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev \
			libffi-dev
COPY ./app /app
COPY ./app/server.crt /
COPY ./app/server.key /
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD python app.py
