It's the last day to meet the quota and you and your team have not collected enough scrap. Thankfully for you, the company is developing a new functionality to their terminal's bestiary and said they might forgive you if you find bugs and vulnerabilities in their new program. Can you make the Company happy?

@bal

from pwn import *
io = remote ("spaceheroes-fsoperator.chals.io", 443, ssl=True, sni="spaceheroes-fsoperator.chals.io")
io.interactive()

sha256sum: 1ef36985c376f0fe2696a599b3f36646e104759718ec30ed5a666c47a57dcb3d
