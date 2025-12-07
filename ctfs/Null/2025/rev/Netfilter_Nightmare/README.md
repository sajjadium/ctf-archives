reverse medium
Author: vektor

I ran a program some friend sent me and all my traffic is now messed up! All this while I was looking at a great steal on the web and can't remember the website(s) I found it on. Help!

Note: By default no traffic passes through the given program.

use sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0 --queue-bypass to send traffic to it.
use sudo iptables -D OUTPUT -j NFQUEUE --queue-num 0 --queue-bypass to delete the previous rule.
