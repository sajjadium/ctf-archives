"""

We have designed a determinstic signature scheme with 
password-based keys, suitable for the post-modern
blockchain. It is resistant to partitioning oracle attacks
and requires no access to randomness under a fixed modulus.
Although not quantum safe, we deem the threat from quantum
attacks to be negligible.

                                        -- The Designers
"""

from hashlib import sha256


def keygen(password):  
    while True:  
        p = 2*random_prime(2^521) + 1
        if p.is_prime(proof=False):  
            break  
    base, h = 3, password  
    for i in range(256):  
        h = sha256(h).digest()  
    x = int.from_bytes(h*2, "big")
    return base, p, pow(base, x, p), x  


def sign(message, priv):  
    h = int(sha256(message).hexdigest(), 16)  
    k = next_prime(int.from_bytes(
        sha256(message + priv.to_bytes(128, "big")).digest() + \
        sha256(message).digest(),
        "big"
    ))
    r = int(pow(g,(k-1)/2,p))  
    s = int(Zmod((p-1)/2)(-r*priv+h)/k)  
    return r, s


g, p, pub, priv = keygen(b"[redacted]") 
r, s = sign(b"blockchain-ready deterministic signatures", priv)


'''

----------------------------------------------------------------------------------------X8
                 
sage: p                                                                                                                                                                                                                                                                                                                                                               
403564885370838178925695432427367491470237155186244212153913898686763710896400971013343861778118177227348808022449550091155336980246939657874541422921996385839128510463
sage: pub                                                                                                                                                                                                                                                                                                                                                             
246412225456431779180824199385732957003440696667152337864522703662113001727131541828819072458270449510317065822513378769528087093456569455854781212817817126406744124198
sage: r                                                                                                                                                                                                                                                                                                                                                               
195569213557534062135883086442918136431967939088647809625293990874404630325238896363416607124844217333997865971186768485716700133773423095190740751263071126576205643521
sage: s                                                                                                                                                                                                                                                                                                                                                               
156909661984338007650026461825579179936003525790982707621071330974873615448305401425316804780001319386278769029432437834130771981383408535426433066382954348912235133967
sage: "midnight{" + str(priv) + "}" == flag                                                                                                                                                                                                                                                                                                                                                                                                                        
True
sage: time
CPU times: user 4 µs, sys: 0 ns, total: 4 µs
Wall time: 6.91 µs
Hammer time: yes

'''
