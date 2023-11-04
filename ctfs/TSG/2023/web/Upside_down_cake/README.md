JA / EN

I checked 413 times to see if the settings are correct.

http://34.84.176.251:12349
Hint for beginners

    First of all, please open the link above and play around with it. This challenge claims that you can get the flag by sending a "very long palindrome" to the server, but it quickly turns out that the story isn't that simple.
    Next, please read the attached source code. Files such as main.mjs and nginx.conf contain the important logic of this website. The flag is stored in a variable called flag, so the purpose is to leak this value.
    Based on these tips, think of a way to get the flag by exploiting some kind of bug instead of sending a "very long palindrome" to the server. Some knowledge of web technologies, especially JavaScript, may be required, so please refer to documentation such as MDN if necessary.
    Note that you do not need a large volume of accesses to solve this problem. As written in the rules, please refrain from mass access similar to DoS.
