A few months ago, I came across <a href="https://devnull-as-a-service.com/">this</a> website. Inspired by it, I decided to recreate the service in C to self-host it.<br>
To avoid any exploitable vulnerabilities, I decided to use a very strict seccomp filter. Even if my code were vulnerable, good luck exploiting it.<br>
PS: You can find the flag at <code>/home/ctf/flag.txt</code> on the remote server.

Author: alex_hcsc