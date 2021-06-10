FROM mcr.microsoft.com/windows/servercore:ltsc2019

COPY /x64.release/ /omnitmizer/

WORKDIR /omnitmizer

RUN icacls flag.exe /setowner "user manager\containeruser"
USER ContainerUser
RUN icacls flag.exe /deny "user manager\containeruser":RX

ENTRYPOINT ["omnitmize.bat"]