FROM mcr.microsoft.com/windows/server:ltsc2022

COPY socat c:/socat/

COPY FlagMail.exe c:/challenge.exe
COPY flag.txt c:/flag.txt

EXPOSE 4444/tcp

ENTRYPOINT [ "c:\\socat\\socat.exe", "-T60", "TCP-LISTEN:4444,reuseaddr,fork", "EXEC:/challenge.exe,pty,raw,stderr,echo=0" ]
