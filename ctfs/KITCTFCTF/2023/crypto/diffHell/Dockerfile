# docker build -t diffhell . && docker run -p 1337:1337 diffhell
FROM sagemath/sagemath:latest

ADD challenge.sage challenge.sage
RUN sudo apt -y update
RUN sudo apt -y install socat
ENTRYPOINT ["socat","-U","TCP-LISTEN:1337,fork","EXEC:'sage challenge.sage'"]
