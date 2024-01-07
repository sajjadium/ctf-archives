You will need to compile and insert the module on your host machine.
Run "make" to compile the kernel module.

To insert the module, run the following commands:
 insmod primer.ko
 mknod /dev/primer c 100 0

Build the docker:
 docker build . --tag primer

Run the docker, passing through the device:
 docker run -v /dev/primer:/dev/primer -p 1337:1337 --privileged -u 0 primer

Connect to your own instance:
 nc 0 1337

To delete the module from your system, run the following commands:
 rm /dev/primer
 rmmod primer
