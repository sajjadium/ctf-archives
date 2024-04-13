Scotty thinks he saw a flag. Help Spock recover it from his memories.

    "Do you know what a mind meld is?"

    "It's that Vulcan thing where you grab someone's head."

from pwn import *
p = remote( 'mindmeld.martiansonly.net',31337)
p.interactive()

md5(scotty) = 599c034e3c3ee871826668b56445fa3c md5(spock) = af9a0b95ce58eb49298ebca374ab5097
