Your goal is to extract the key used for the encryption of the captured data.

All blocks have been encrypted in Electronic Codebook (ECB) mode.
All data blocks are in hexadecimal, byte 0 first, byte 15 last. First column: 128 bits input block, second column: 128 bits encrypted block, third column: encryption time.
The key length is 128 bits.
The format of the flag is N0PS{key} where key is the 32 digits hexadecimal representation of the secret key you found, byte 0 first, byte 15 last, with everything in capital letters.

If the correct key was 0102030405060708090A0B0C0D0E0F the following command would output the first ciphertext bloc in ta.dat: printf "$(sed -n 's/ .*//;s/\(..\)/\\x\1/gp;q' ta.dat)" | openssl enc -aes-128-ecb -nosalt -nopad -K 0102030405060708090A0B0C0D0E0F | od -v -A none -tx1
