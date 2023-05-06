FROM mcr.microsoft.com/windows/servercore:ltsc2019
RUN net user /add pwn
RUN mkdir \chal
RUN mkdir \x86
COPY BabyWindows.exe \chal
COPY BabyWindowsLib.dll \chal
COPY flag.txt \chal
COPY socat-1.7.3.0-windows-master .
RUN ICACLS c:\chal /deny pwn:(WD,AD) /t /c
USER ContainerAdministrator
RUN SETX Path %Path%;C:\socat-1.7.3.0-windows-master /M
RUN SETX Path %Path%;C:\chal /M
USER pwn
EXPOSE 7777
CMD ["socat.exe", "-T120", "TCP-LISTEN:7777,reuseaddr,fork", "exec:BabyWindows.exe,pty,ctty,echo=0"]
