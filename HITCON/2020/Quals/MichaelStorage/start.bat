reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\MichaelStorage.exe" /v FrontEndHeapDebugOptions /t REG_DWORD /d 0x8 /f
AppJailLauncher.exe ./MichaelStorage.exe /timeout:12000000 /key:flag.txt /port:56746
