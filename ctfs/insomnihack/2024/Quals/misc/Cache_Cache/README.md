by itm4n

Your target is a Windows service, accessible through the host cachecache.insomnihack.ch on TCP port 80. Your objective is to read the content of the file flag.txt which is stored in the application's directory.

    The target service consists of a single executable: "Server.exe".
    The binary file contains hints that should help reverse engineering.
    No enumeration required on the front web server, it is just a proxy.
    No bruteforcing required.

Provided assets:

    Server executable: Server.exe
    User credentials : winternals / Insomni'h4ck
