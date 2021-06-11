Remy set up a blackjack server where friends and students can win Xavier coins to spend around the campus, but someone broke in and stole a bunch of coins (he thinks it was Silas Burr) and he needs help figuring out how.

nc challenges.ctfd.io 30466

Hank didn't have time to figure it out, but he said this may come in handy: https://libc.nullbyte.cat/

if you're having trouble maintaining a shell, try using cat to keep stdin open:

#(cat ./exploit ; cat - ) | nc xxxx yy

or

#(python sploit.py ; cat - ) | nc xxxx yy

etc...

