FROM python:3.11
RUN pip3 install flask
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs
WORKDIR /app
COPY package*.json ./
RUN npm i
COPY static/ ./static/
COPY flag.txt app.py keychecker.devs ./
EXPOSE 80
CMD ./node_modules/@devicescript/cli/devicescript devtools & flask run -h '0.0.0.0' -p 80 --with-threads
