FROM node:20.5.1

COPY ./src /app

COPY flag.txt /flag.txt

WORKDIR /app
RUN chmod +x run.sh
RUN npm install

RUN useradd -ms /bin/bash user
USER user

ENTRYPOINT ["./run.sh"]