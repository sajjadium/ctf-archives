characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}~_"
flag = "lactf{REDACTED~}"

def bigram_multiplicative_shift(bigram):
    assert(len(bigram) == 2)
    pos1 = characters.find(bigram[0]) + 1
    pos2 = characters.find(bigram[1]) + 1
    shift = (pos1 * pos2) % 67
    return characters[((pos1 * shift) % 67) - 1] + characters[((pos2 * shift) % 67) - 1]

shifted_flag = ""
for i in range(0, len(flag), 2):
    bigram = flag[i:i+2]
    shifted_bigram = bigram_multiplicative_shift(bigram)
    shifted_flag += shifted_bigram
print(shifted_flag)
# jlT84CKOAhxvdrPQWlWT6cEVD78z5QREBINSsU50FMhv662W
# Get solving!
# ...it's not injective you say? Ok fine, I'll give you a hint.
not_the_flag = "mCtRNrPw_Ay9mytTR7ZpLJtrflqLS0BLpthi~2LgUY9cii7w"
also_not_the_flag = "PKRcu0l}D823P2R8c~H9DMc{NmxDF{hD3cB~i1Db}kpR77iU"
