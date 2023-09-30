ath0

This is really, truly, the most horribly unsafe thing you can do in Rust. The guardrails here are dental floss.

    The Rustmonicon


chat
=====

Important: the client is vulnerable (and has the flag). We do not recommend connecting the client to untrusted servers. The instancer is designed so that only you (your IP) can connect to your server instance, but you are using the client at your own risk.

If you want to replicate the full remote (instancer) setup:

```
    docker-compose up
```

You are not intended to exploit the instancer, so its operation is explained here:

- Connect to the instancer the IP and port specified in the challenge description.
- The instancer will direct you to another port, where the `server` binary is listening.
- The instancer will then immediately connect the `client` to the same server.

You are provided with the stdout of the `server`.

```
== proof-of-work: disabled ==
[*] Queued in position 0
[+] Handling your job now

[*] ip = 34.192.121.82
[*] port = 7002

[*] This instance will stay up for 300 seconds
[*] Starting...
Listening on port 8000
[*] Client IP: 10.0.5.2
New connection from Ok(10.0.5.2:39596)
```

The private Client IP is provided just so you can identify that the client has in fact connected (the line following that shows the client is up). You are not expected to use the client IP for anything else.
