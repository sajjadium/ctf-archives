kernel, extreme
We found my brother's old iMac but forgot the password, maybe you can help me get in?
He said he was working on something involving "pointer authentication codes" and "a custom kernel"? I can't recall...
Attached is the original Snow Leopard kernel macho as well as the kernel running on the iMac.
Notes
Note that we have backported patches for several known Snow Leopard N-Days! It is our belief that the easiest way to solve this challenge is the intended solution.
If you want to create an image for local testing, follow the instructions here:
https://github.com/jprx/how-to-install-snow-leopard-in-qemu
Make sure you disable journaling so that you can edit the filesystem from your host if something breaks!
Inside the VM, rename /System/Library/Extensions/AppleProfileFamily.kext to AppleProfileFamily.kext.bak.
Delete /mach_kernel and replace it with the attached mach_kernel.sigpwny file (saved as /mach_kernel).
Reboot the VM and then run uname -v, you should see the version string of sigpwny:xnu-1456.1.2.6/BUILD/obj//RELEASE_X86_64.
Install Xcode 3.2 (xcode3210a432.dmg) inside the VM to get gcc.
Connecting to Our Instance
Password for the user user is user. Flag is ravi's password. The flag is also at /flag. You can also ssh into the remote machine by (inst-1234567890123456 is the ID of your instance):
