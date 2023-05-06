FROM csgo_server
SHELL ["cmd", "/S", "/C"]
WORKDIR C:/windbg
RUN curl -fSLo windbg.msi "https://download.microsoft.com/download/4/2/2/42245968-6A79-4DA7-A5FB-08C0AD0AE661/windowssdk/Installers/X86%20Debuggers%20And%20Tools-x86_en-us.msi"
RUN windbg.msi
WORKDIR C:/Program Files (x86)/Windows Kits/10/Debuggers
RUN copy x86 C:\\windbg 
WORKDIR C:/csgo-ds
CMD C:/windbg/dbgsrv.exe -t tcp:clicon=%IP%,port=%PORT%