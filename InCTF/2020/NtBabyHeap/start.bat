powershell set-ProcessMitigation -Name NtBabyHeap.exe -Enable DisallowChildProcessCreation
AppJailLauncher.exe ./NtBabyHeap.exe /timeout:12000000 /key:flag.txt /port:13337
