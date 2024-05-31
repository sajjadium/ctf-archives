13x1

Maybe using Inspect Element will help you!

    Small hint: If you're struggling with reproducing it on remote, you can use socat to proxy the remote instance to localhost:1337 like this:

    socat TCP-LISTEN:1337,fork OPENSSL:xxx--xxx-1234.ctf.kitctf.de:443

    and it should behave exactly like a locally running docker container.
