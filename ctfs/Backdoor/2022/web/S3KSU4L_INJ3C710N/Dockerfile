FROM ubuntu:20.04
RUN apt-get update 
RUN apt-get install -y python3 python3-pip 
WORKDIR /src/app
COPY ./chall/ .
RUN rm flag.txt
RUN pip3 install -r requirements.txt
CMD [ "python3", "main.py" ]
EXPOSE 16052