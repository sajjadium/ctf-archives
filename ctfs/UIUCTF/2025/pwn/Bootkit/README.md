Many years later, in a galaxy far far away, the Empire of UIUCTF was collecting UEFI patches for their secret lab machines, and stumbled upon the remains of SIGPwny Inc. and PwnySIG Inc. Not knowing the dangers, they installed both patch sets to their super secure lab machines, with TPM-sealed disk encryption protecting their latest research (flag).

As the lead security officer of the rebellion against the Empire, you need their research to expose the Empire of their anti-droid vendetta. Unfortunately, you discovered that the Empire designed the secret disks such that they detach themselves as soon as any keyboard input is detected during boot, and since you need the keyboard to install the bootkit, the bootkit must survive the reboot. TPM also hashes everything on the boot disk and there's no hope of keeping the bootkit there.

That leaves only one option, completely and utterly pwning the firmware...

Lua.efi, but with persistance. SMM is Aleep, but with purpose.

author: YiFei Zhu
