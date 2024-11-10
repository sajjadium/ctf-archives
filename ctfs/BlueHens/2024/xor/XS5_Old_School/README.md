xor bad prng deduction meta guess school

I used an old, common, prng. Knowledge of the solvability of this problem helps you deduce...

https://gist.github.com/AndyNovo/40adab2061f6b2fd47d6ba7d765fb159

(this flag is udctf{...} not UDCTF{...})

P.S. I would never want you to think of a problem as guessy, if you think this is guessy I encourage you to reserve judgement and do this one AFTER the other ones.

HINT: Out of all the insecure PRNGs this one is the only one that can be broken using just 6 bytes mod 256 without any other insights, and it's the oldest school popular PRNG. If you pretend you have the first byte of the flag at spot i you'll get a byte mod 256 from the PRNG and can check the candidates from the prng and confirm the next character too. I know it's not too tough to validate this PRNG and the location of the flag, which also limits the list of insecure PRNGs. Once you know the prng there's only a couple ways the implementation could be done, still sensible in this context, and reasonable.

This series of problems is called the XOR SCHOOL. For whatever reason I just love xor problems and over the years there are many that have charmed my soul. This sequence is an homage to the many many ways that xor shows up in CTFs. I hope you can see some of the beauty that I see through them. -ProfNinja
