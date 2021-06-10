There is a patched [clamav](https://github.com/Cisco-Talos/clamav-devel)(commit id: `6c11e824a794770c469f3a46141d5ea7927b6ea6`) running on ubuntu:18.04.

Everytime you upload your payloads, we will scan these with the following commands
```bash
clamdscan your_upload_file
clamscan your_upload_file
```
Try to pwn this antivirus software.