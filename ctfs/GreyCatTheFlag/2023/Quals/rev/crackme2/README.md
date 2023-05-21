Hope you like this.

Update: The previous version of crackme2 is unstable. Please download the latest version here.

If you aren't using Ubuntu 22.04, you will have to use the supplied libc, by downloading the libc and ld binary into the same directory as the crackme binary.

LD_LIBRARY_PATH=. ./ld-linux-x86-64.so.2 ./crackme2-2 "grey{aaa}"

You may consider using pwninit so that you can run the binary directly without the long line above.

Update 2: crackme2-old is the previous version that is unstable. You may use this if you do not want to use ld to run the binary.

Also, the flag format is grey{...} instead of greyctf{...} as mentioned by the program.
