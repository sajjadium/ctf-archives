Your friend got infected with a deadly virus. Can you develop a vaccine to save his precious files?
IMPORTANT

This is a real ransomware. If you run it on your computer, it will encrypt all your files. Please be careful ;). If you somehow do encrypt your files, we provide a decryption executable which you can use to hopefully save your files.

The password for the zip is ALLES!_inf3ct3d
Info

The public and private images have 2 differences. The flag and a constant in the Ransom.exe file. This change shouldn't affect your exploit. The endpoint shouldn't be considered part of the challenge.

To start the ReactOS VM use this command:

qemu-system-x86_64 -m 128 -hda ReactOS_public.qcow2 -device e1000,netdev=net0 -netdev user,id=net0,hostfwd=tcp::1024-:31337

Don't panic when requesting a session, it can take about a minute for the session to be live.
Hint

I heard the ransomware stopped working after trying to encrypt the file with the following content:

RANDOM_NUMBER=38274637672367813412783182787312878321732717321878327
