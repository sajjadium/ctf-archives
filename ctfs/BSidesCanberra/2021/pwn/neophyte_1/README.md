Welcome to neophyte. This is a set of 11 challenges designed to walk you through the process of solving a pwn challenge. We will briefly touch on reverse engineering, vulnerability research and exploit development. Once you solve a challenge the next will appear when the challenge page refreshes or press F5.

Like most pwn CTF challenges, you are given an executable binary. This one runs on linux, and is an Executable and Linkable Format (ELF) binary.

Binary files make sense to computers and operating systems, but are hard for humans to understand. To aid this, we can parse the executable format headers and convert machine instructions to assembly instructions. Assembly is a low-level programming language heavily tied to underlying computer architecture instructions. The process of converting machine code to assembly instructions is called disassembly. Whilst assembly representation allows a reverse engineer to understand a binary, in cases where the binary was compiled from a higher level language like C, we can potentially aid the reverse engineer further by decompilling the assembly code into high level source code. This process is lossy, so the output is often called pseudo code. To analyse (reverse engineer) this binary, you could use a number of tools, but we will focus on Ghidra. It's free, has both a decompiler and disassembler, and is awesome. You can get Ghidra here and follow the installation guide. The Ghidra homepage also has a quick start video, you should watch this if you are not familiar with Ghidra.

Once you have Ghidra installed, you need to create a new project (Ctrl + N) and import the neophyte binary as a file (I). Accept the defaults for the import. After clicking OK on the Import Results Summary you will be taken back to the Tool Chest. Now you can disassemble and decompile the binary by doing the following:

    Right click neophyte -> Open in default tool
    Click Yes then Analyze to analyze

Now you are presented with the code browser displaying information from the neophyte binary. It can be a bit daunting, but Ghidra will open up with the main window focussed on the start of the binary, which contains the ELF headers as outlined in the Wikipedia article.

When the operating system executes a binary, one the of most important jobs is to work out where to start execution instructions in the target binary. It does this by reading the e_entry field in the ELF headers.

The flag is the address pointed to by e_entry.

Hint: Use Ghidra to find this. Ghidra will helpfully name this location as a function labeled _start.

You could get this value by reading the bytes on this initial screen for the e_entry field (be careful as x86 is little-endian). Your other option is to double-click start and read the memory address from the left hand side of the Listing window. This is the number in black (for default color settings).

neophyte questions do not use the cybears{} flag format. If you're having trouble submitting a flag which you think is correct, speak to an admin.

The format for this flag is either decimal (54321), or hexadecimal (0x12345).
