FROM ubuntu:18.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update -y
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt upgrade -y
RUN apt install -y python3.6
RUN apt install -y python3-pip
RUN apt install -y unoconv
RUN pip3 install flask
RUN pip3 install flask_sqlalchemy
RUN pip3 install PyJWT==1.7.1
RUN pip3 install argparse
RUN pip3 install PyPDF2
RUN pip3 install reportlab
RUN mkdir app
WORKDIR /app
COPY . .
RUN mv flag /flag
CMD python3 app.py
