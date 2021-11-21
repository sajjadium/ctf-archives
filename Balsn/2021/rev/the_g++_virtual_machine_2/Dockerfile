FROM gcc:11.2.0

COPY ./src /src

RUN apt-get update; apt-get install -y libboost-all-dev; exit 0

CMD "/bin/bash"
