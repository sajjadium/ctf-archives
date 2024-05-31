13x1

⚠️ Important: This challenge requires a special setup to play! Please read the full description!

I heard that XZ was backdoored, so I replaced the weird binary with a new test file. I hope it's not backdoored again, because I have an SSHD running...

To play this challenge, you need to connect via SSH instead of HTTP or raw TCP! Unfortunately, due to SSH not supporting TLS, you need to use socat to encrypt your traffic. The instancer will give you an instance like xxx--xxx-1234.ctf.kitctf.de, and you need to run this with your instance to connect:

socat TCP-LISTEN:2222,fork OPENSSL:xxx--xxx-1234.ctf.kitctf.de:443

Then you can connect with your SSH client to that port. And to make your life easier, you can use these options to disable strict host checking:

ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -p 2222 root@localhost

Also, you do not need a very powerful CPU/GPU to solve this challenge! The intended solve is done in under a second on my laptop, you do not need excessive amounts of brute force to solve it.
