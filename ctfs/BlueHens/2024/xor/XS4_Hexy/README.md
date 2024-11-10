xor

In [1]: xor(flag + key + hashlib.sha256(flag).hexdigest().encode(), key).hex()
Out[1]: '1a0c43191f5b15485d5a31574e4333141a5d073a0840541f560b515324001d00000c5315000e0a4e0452111618060654080154414b09165147791f1941041b07115816454b060b5e5a20094d135e101516425506420145544c18570d11541a4255125a5a5e5212470f050b5b425d1b434409034c5a19615c46465a424b151906041852415648415b5a44'

This series of problems is called the XOR SCHOOL. For whatever reason I just love xor problems and over the years there are many that have charmed my soul. This sequence is an homage to the many many ways that xor shows up in CTFs. I hope you can see some of the beauty that I see through them. -ProfNinja
