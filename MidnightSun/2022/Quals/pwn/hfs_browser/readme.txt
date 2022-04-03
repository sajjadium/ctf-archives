Please only test your exploit against the remote service once it works locally :prayer:

How to test locally:
LD_PRELOAD="./libc-2.31.so ./libcurl-gnutls.so.4.6.0" ./hfs_browser http://127.0.0.1:8081/pwn.js

For GDB:
- gdb --args env LD_PRELOAD="./libc-2.31.so ./libcurl-gnutls.so.4.6.0" ./hfs_browser
- r http://127.0.0.1:8081/pwn.js

Tip #1
You might need this: git clone https://github.com/svaarala/duktape -b v2.5-maintenance
Tip #2
Check the HFS SUPER SECURE TM patch in duktape.diff
Tip #3
Serve your exploit: python3 -m http.server --bind=0.0.0.0 8081

NOTE: The curl version is irrelevant for the challenge. It is only in the archive to provide all dependenices (hopefully :-))
NOTE: The hfs_browser has full symbols so you can use ptype and so on
NOTE: Docker OS version: ubuntu:20.04