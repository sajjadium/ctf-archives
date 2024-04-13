You're out of space fuel! Luckily some dope left his alien credit card on the ground outside the ATM at the dark matter station. It has a weird aura though. Oh well! Fill up your tank so you can keep moving!

from pwn import *
p = remote("spaceheroes-atm.chals.io", 443, ssl=True, sni="spaceheroes-atm.chals.io")
p.interactive()

md5(atm.bin)= a9bc824d0ee34a041a3a8cb036bb0701
