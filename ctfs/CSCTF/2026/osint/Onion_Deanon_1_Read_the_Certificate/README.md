OSINT
Easy
covert-security
AUTHOR
Covert Security
MISSION
BRIEFING
🧅 A hidden service hides where a server is, but only for as long as that server never says anything about itself anywhere else. ParsnipLocker is a ransomware crew that runs its leak blog as a Tor hidden service over HTTPS. Whether their anonymity investment holds up is for you to find out.
Scope: a simulated environment operated by Covert Security. Reach the onion service with Tor Browser. Stay passive — no port scan, brute force or probing. Only the single host you identify is in scope.
Ransom note recovered from an infected workstation:

=== YOUR NETWORK HAS BEEN PARSNIPPED ===
Hello, Globex Artisanal Mayonnaise Co.
Your files are encrypted. Your backups are gone.
You have 72 hours. Pay 0.8 XMR or we publish everything you own on our blog. Tor Browser required:
Case ID: PL-0091
ParsnipLocker

Task 1 — Read the Certificate
Inspect the certificate presented by the ParsnipLocker leak blog.
Answer: the certificate serial number, uppercase hexadecimal, no colons or spaces.
Flag format: CSCTF{<answer>}
