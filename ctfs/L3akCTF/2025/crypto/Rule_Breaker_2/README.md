If you thought rules were easy after the last challenge, think again! I've concocted more devious password mangling rules to push the limits of your cracking knowledge (and possibly your CPU...):

    Password 1: Prepend 1 uppercase letter, Swap the first 2 characters, Rotate it to the right 3 times, Append a 4-digit year since 1900.
    Password 2: Lowercase the entire password. Apply a random caesar cipher shift to all the letters in the password. Then, replace each alphanumeric character with its right neighbor on the QWERTY keyboard. Finally, reverse it.
    Password 3: Split the password in half, toggle the case of every consonant in the first half, randomly toggle the case of all vowels in the second half, then interleave the halves together. Assume password has an even length and is no more than 14 characters. The letter Y is considered a vowel for the purposes of this challenge.

2a07038481b64a934495e5a91d011ecbf278aba8c5263841e1d13f73975d5397 cd6e58d947e2f7ace23cb6d602daa1ae46934c3c1f4800bfd25e6af2b555f6f5 84b9e0298b1beb5236b7fcd2dd67e67abf62d16fe6d591024178790238cb4453

Use the rockyou.txt wordlist.

Flag format: L3AK{pass1_pass2_pass3}

Author: Suvoni
