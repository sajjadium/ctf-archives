FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update --fix-missing && apt-get -y upgrade
RUN apt-get -y install python3-pip
RUN python3 -m pip install flask pycryptodome
ENV FLASK_APP=app
USER daemon
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]
