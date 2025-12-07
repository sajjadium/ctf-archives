reverse hard kernel windows
Author: tomadimitrie

I installed the driver for my printer, but my printer is still not working. However, some apps have started behaving weirdly, like the one I attached. It only works when the driver is running and is asking me for a… flag? What does that mean?

Note 1: You need a VM with testsigning enabled. Do NOT do that on your host machine. Steps:

disable Secure Boot
bcdedit.exe /set testsigning on
bcdedit.exe /set debug on
bcdedit.exe /set loadoptions DDISABLE_INTEGRITY_CHECKS
reboot
Note 2: Install the driver with devcon.exe install ConfusionKM.inf root\confusionkm. You can get devcon by downloading the WDK and copying it from C:\Program Files (x86)\Windows Kits\10\Tools\<version>\x64\devcon.exe. The WDK is safe to install on your host machine and devcon can be safely copied to the VM with no other dependencies required.
