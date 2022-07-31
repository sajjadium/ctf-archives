FROM python:3

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# create user
RUN groupadd chalusr
RUN useradd -ms /bin/bash -g chalusr chalusr

# pip
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# chal files
RUN mkdir static templates
COPY app.py cipher.py flag.enc ./
COPY templates/ ./templates/

USER chalusr
CMD [ "python3", "app.py" ]

