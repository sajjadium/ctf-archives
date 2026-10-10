SR

A workstation got imaged late one night and three leftovers from its print spooler made it out before the drive was wiped. A scanner in the evidence room had a scan of what looks like the same page sitting on it. Prove the document was printed from that exact machine, then build the flag.

The flag is not sitting in any file. You build it from three things you have to recover: the username that owned the print job (lowercased), the printer's 7 digit serial number, and the UTC timestamp of the print, formatted YYYY-MM-DDTHH:MM:SSZ (seconds are always 00). The flag is then isfcr{ followed by the first 16 hex characters of SHA-256(username + "|" + serial + "|" + timestamp) followed by }.

You are given FP02CF4.SHD, FP02CF4.SPL, and scan.png. Everything you need to recover those three values is in those files.
