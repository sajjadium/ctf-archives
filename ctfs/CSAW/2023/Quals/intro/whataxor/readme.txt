Reversing is hard. But, I hate to break it to you, you haven't really been reversing up to now.

This program still has the flag embedded in it, but now it's obfuscated.

You'll need to figure out:
 1. What the program is doing
 2. How it obfuscates the flag
 3. How you can recover the flag

You can use `objdump` to read the raw disassembly of the file, but that's extremely complicated.
Instead, let's use a tool that'll simply the output for us. I recommend a free decompiler, like:
 - Dogbolt (lets you see the output of many tools at once): https://dogbolt.org/
 - Binary Ninja Demo or Cloud (cloud lets you collab with your team members!): https://binary.ninja/demo/
 - Ghidra (though setting up Java can be a pain): https://ghidra-sre.org/
 - IDA Free: https://hex-rays.com/ida-free/
