# Walkthrough of Intro to GDB

### What is dynamic analysis?
> Dynamic analysis is a type of analysis that requires live execution of the code. If, for example, we encounter a code that decrypts or decompresses to a huge amount of data, and if we want to see the contents of the decoded data, then the fastest option would be to do dynamic analysis. We can run a debug session and let that area of code run for us.

### What is GDB?
> GDB (GNU DeBugger) is the bulit in Linux debugger on the GNU framework, basically everything Linux uses. It allows the reverser to step through a program and analyze in the inner working of that program in runtime. More advanced features included in GEF and other extensions allow for a more comprehensive view of the binary.

### How do computers run a binary?
> Computers use something called the **stack** to store information while a program is running by **pushing** and **popping** values off the top. This type of memory is different from the memory in hard drive/SSD as the stack uses data storages known as **registers** which can store 4 bytes in a 32-bit system and 8 bytes in a 64-bit system (EAX vs RAX). These registers interact with the RAM (Random Access Memory) using memory address **pointers** and constitute the major components of the CPU (central processing unit).

### How do I use GDB?
> Installing GDB: GDB should be built into any function Linux image but if you don't have a Linux image refer to [here](https://brb.nci.nih.gov/seqtools/installUbuntu.html).

> GDB disassembles a compiled binary into **Assembly**, a coding language based on simple **opcodes** and **operants**, a bit (a lot) different from what people traditionally think of as a "coding language", C, Python, Java, etc.. A quick guide for Assembly can be found [here](https://medium.com/reverse-engineering-for-dummies/a-crash-course-in-assembly-language-695b07995b4d). GDB uses **stepping** to move through a live binary and allows the reverser to view all the moving components and their values, namely: registers and memory locations. A great tutorial for using GDB can be found [here](https://www.youtube.com/watch?v=svG6OPyKsrw&t=2s) though it is slightly longer (but you can always watch at 2x speed ;)) or [this article](http://www.cs.toronto.edu/~krueger/csc209h/tut/gdb_tutorial.html).

### Examples:
> [Bomb Labs write up](http://zpalexander.com/binary-bomb-lab-set-up/)
> [String compare write up](https://github.com/HackThisSite/CTF-Writeups/blob/master/2016/SCTF/rev1/README.md)
> [Crackmes write up](https://infosecwriteups.com/tryhackme-reversing-elf-writeup-6fd006704148)

### Regards
> If you still can't get the solution try Googling for other examples to understand theory and if you're still stuck just shoot me a ticket through the Discord Ticket bot. I wish you all the best on these challenges and I hope you enjoy your time trying to crack not only my challenges, but the rest of my team's. Good luck and have fun :D ~ BrokenAppendix