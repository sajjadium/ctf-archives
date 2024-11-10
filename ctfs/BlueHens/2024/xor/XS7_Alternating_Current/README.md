In [5]: cipher = DES.new(ky, DES.MODE_OFB)

In [6]: cipher.encrypt(msg).hex()
Out[6]: 'ee73f99771135c984db42bc9e3e73148fc60add1484c4bcc1f8269b6e5b06163de5ecfe85e2049975cb333b6e1b06657c570afce64021d9e03b9789dfeea211cf368bcda780d58df00b82b9af7e4371cf375bcd4760c58df04a97881f3ef224fba62f3c237085491'

This series of problems is called the XOR SCHOOL. For whatever reason I just love xor problems and over the years there are many that have charmed my soul. This sequence is an homage to the many many ways that xor shows up in CTFs. I hope you can see some of the beauty that I see through them. -ProfNinja
