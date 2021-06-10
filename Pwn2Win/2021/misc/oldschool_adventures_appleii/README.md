We found this Rhiza's Government Server, and we need to access it! It runs an Apple II emulator and accepts codes in Applesoft BASIC. If the result of your code generates a valid QR Code standard (not micro QR), it will be read and the content will be executed as a shell command on the Linux system. A very interesting way to interact with a server, don't you think?

Follow the directives below:

    Maximum size of the payload: 268 chars (it will be truncated at this point)
    Send the entire payload in one line (only printable chars), replacing line-break with the symbol § (only 1 allowed)
    Only QR Codes are accepted (not micro QR)
    Your code can take up to 50 seconds to be drawn, before the QR Code verification occurs
    If you have any questions, take a look at the source code of the server inside the container

We are releasing two options for you to run the environment and do your tests locally.

Docker:

$ docker-compose up
$ nc localhost 1337

Docker Files

LXC Container:

$ lxd init and some <Enters> (if you've never used it before)
$ lxc image import <name>.tar.gz --alias oldschool
$ lxc launch oldschool oldschool
$ lxc list (to get the IP)
$ nc IP 1337

LXC Files
