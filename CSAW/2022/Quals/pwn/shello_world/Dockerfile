FROM mcr.microsoft.com/windows/servercore:ltsc2019
RUN net user /add pwn
RUN mkdir \chal
COPY ShelloWorld.exe \chal
COPY ShelloWorldLib.dll \chal
COPY flag.txt \chal
COPY socat-1.7.3.0-windows-master . 
RUN ICACLS c:\chal /deny pwn:(WD,AD) /t /c
USER ContainerAdministrator
RUN SETX Path %Path%;C:\socat-1.7.3.0-windows-master /M
RUN SETX Path %Path%;C:\chal /M
USER pwn
EXPOSE 7778
CMD ["socat.exe", "-T120", "TCP-LISTEN:7778,reuseaddr,fork", "exec:ShelloWorld.exe,pty,ctty,echo=0"]
