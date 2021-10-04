FROM ghcr.io/google/nsjail/nsjail:latest

RUN mkdir /server


RUN apt-get update && apt-get upgrade -y && apt-get install -y hashcash wget dpkg  python3.8 xinetd gawk && \
    wget https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    rm packages-microsoft-prod.deb && \
    apt-get update && apt-get install -y apt-transport-https && apt-get update && apt-get install -y dotnet-sdk-5.0  && \
    dotnet new console -o test && rm -rf test


COPY ./src/*.sh  /server/
COPY ./src/*.py /server/
COPY ./src/template.cs /server/
COPY ./src/proj_template /server/proj_template
COPY ./src/xinetd.conf /etc/xinetd.d/ctf
RUN chmod 777 /server/*.sh 


WORKDIR /server/
EXPOSE 2000

CMD ["xinetd", "-dontfork", "-f", "/etc/xinetd.d/ctf"]
