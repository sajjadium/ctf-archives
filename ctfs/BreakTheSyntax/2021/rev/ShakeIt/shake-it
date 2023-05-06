#!/usr/bin/ruby

# Just converts string to int like
# ABC => 0x414243
# CTF => 0x435446
# [1] pry(main)> (str2int 'AAAA BBBB CCCC DDDD')
# => 1455232941411221895323142643903423937501217860
# [2] pry(main)> (str2int 'AAAA BBBB CCCC DDDD').to_s(16)
# => "41414141204242424220434343432044444444"
def str2int x
    return x.unpack("H*")[0].to_i(16)
end

# Same, but backwards
# [3] pry(main)> int2str 1455232941411221895323142643903423937501217860
# => "AAAA BBBB CCCC DDDD"
def int2str x
    return [x.to_s(16)].pack("H*")
end

def uber_hash_function x
    x = str2int x
    
    x = x ^ (x >> 3);

    return x.to_s(16)
end

dummy_flag = "BtS-CTF{A_BB_CCC_DDDD_EEEEE_FFFFFF}"
dummy_hash = uber_hash_function dummy_flag
# dummy_hash = "4a3ad948eb3eceb42974aa0a14ab2b2b34acccccccd4adededededf4ae8e8e8e8e8eb2"

puts "Hash for string #{dummy_flag} is #{dummy_hash}"