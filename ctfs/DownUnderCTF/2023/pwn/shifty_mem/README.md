Shifting as a SUID binary service, because why not?
Note: This challenge runs over TLS on port 443. You can connect with openssl (openssl s_client -quiet -connect <hostname>:443) or pwntools (remote('<hostname>', 443, ssl=True)). This shouldn't affect exploitation.
