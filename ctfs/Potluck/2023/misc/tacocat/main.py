#!/usr/local/bin/python
while True:#
    x = input("palindrome? ")#
    assert "#" not in x, "comments are bad"#
    assert all(ord(i) < 128 for i in x), "ascii only kthx"#
    assert x == x[::-1], "not a palindrome"#
    assert len(x) < 36, "palindromes can't be more than 35 characters long, this is a well known fact."#
    assert sum(x.encode()) % 256 == 69, "not nice!"#
    eval(x)#)x(lave    
#"!ecin ton" ,96 == 652 % ))(edocne.x(mus tressa    
#".tcaf nwonk llew a si siht ,gnol sretcarahc 53 naht erom eb t'nac semordnilap" ,63 < )x(nel tressa    
#"emordnilap a ton" ,]1-::[x == x tressa    
#"xhtk ylno iicsa" ,)x ni i rof 821 < )i(dro(lla tressa    
#"dab era stnemmoc" ,x ni ton "#" tressa    
#)" ?emordnilap"(tupni = x    
#:eurT elihw
