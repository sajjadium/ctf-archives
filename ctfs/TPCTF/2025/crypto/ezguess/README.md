Dear hacker:

Here are some information we have gather for you:

    Li Hua, a Chinese man, born on May 17, 1995.
    His Japanese girlfriend Sato Chika born on November 23, 1996.
    Li is not particularly security-conscious; He tends to use personal information in his passwords.

We have recovered some of his personal passwords from a database, but only in hashed form.

Crack the passwords, and get your flag.

hash = hash_fn(salt + data)
salt = 'TPCTFS@lt'
hash(pwd1) = 0fe6cac6ffe50948f63e706be0d54141 MD5 [0-9]{4}
hash(pwd2) = de77895388426cdf447309b0d9d4871e MD5 [0-9]{6}
hash(pwd3) = fa88d7405eec5cb8dd31895a14d35675e36d58ac SHA1 [a-z0-9]{12}
hash(pwd4) = a672d2d87867b5ebfca00bcdc20c869ddf4b56f8 SHA1 [a-zA-Z0-9]{10,12}
hash(pwd5) = dfc2733184f99530174cddfffaaec0d8841256b7c09d21aef3b4b43237333807 SHA256 [a-zA-Z0-9.]{12,14}

SHA256_hash = SHA256([pwd1,pwd2,pwd3,pwd4,pwd5].join(''))
flag = TPCTF{SHA256_hash}
