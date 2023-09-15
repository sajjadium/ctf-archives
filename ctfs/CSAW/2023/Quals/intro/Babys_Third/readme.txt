Reversing is hard. This time moreso than the last, but now by much.

This file is a compiled executable binary (which we refer to as just "binary" for short).

The process of compiling code is extremely complicated, but thankfully you don't need to know much about it to solve this challenge. At a high level, the source code is getting translated from a human-readable text file (not provided) to something much harder to read.... Try `cat`ing the file; it don't work so good. Much of the data in the program is encoded in such a way that makes it easier for the computer to understand - but there are still some elements in there intended to be interacted with by the user. So the question becomes "How do we extract that information?" And eventually "How to we better display that information intended for the computer to understand for a human to understand instead?" But that next question is for the next challenge...

And like we have tools for working with text (such as text editors, `cat`, whatever you're reading this in), there are tools for working with binaries as well. In Linux (it will be helpful to have a Linux VM or Linux system to run these programs in, though technically not required), you can install "bin utils". Most notably, binutils includes `objdump` and `strings`. One of those are what you need to solve this challenge...

Remember, the first rule of reading code is:

DON'T

READ

THE

CODE

(just read the important bits... 👀)