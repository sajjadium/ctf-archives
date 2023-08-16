The CSCG qualification, a big german hacking competition, featured the challenge Honk! Honk!, exploiting the GOOSE server of the libiec61850. Now, it is not "Honk Honk!" anymore. You still need to exploit a 0-day in the libiec61850, but this time in the libiec61850 client.
Some notes:
You will get access to a server via SSH. You can even use SCP to upload your exploit.
Every second, the following command will run as root: ./mms_utility -p 1337 -d -i -f -m
If you have problems to SCP your exploit into the container, try scp -P 31222 -O [...].
