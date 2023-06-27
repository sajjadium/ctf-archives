Exactly when we thought PHP is dead: The mighty elephant strikes back with a JIT Engine :D
I wasn't satisfied with all the extra assembly the JIT compiler of PHP8 generates, so I made a new function to cut off some of it for better performance. I hope this won't break the security of my php service.
Do you think you have what it takes to escape the sandbox?


# Zen(d) Master

Hello players! :D 

Some notes on the challenge:

* You got a hardened PHP environment, your task is to break out of the sandbox.
* This is a pwnable chall, you should **not**(by any chance) try to pwn the applicative layer of if(such as: the python layer, etc.)
* Anything that is related to the `opcache.preload` and `opcache.preload_user` directives (in `conf.ini`) is not related to the chall. These lines are there due to some CTF infra requirements. Don't bother spending your time on understanding this when you're trying to spot the bug.

gl hf
