Set-ProcessMitigation -Name EasyVM.exe -Enable DisallowChildProcessCreation
./AppJailLauncher.exe ./EasyVM.exe /timeout:120 /key:flag.txt /port:9999
