                                    Overview
                                    --------
Hello fellow exploit developer. We have a bug in the MuJS JavaScript engine that
we want you to exploit. Your exploit should be robust! It shouldn't rely on
binary offsets that will change between builds of the same code, and it should
expose a clean, architecture independent API.

Your exploit needs to implement:

    read32(address)         - Read an arbitrary 32-bit value from `address`.

    write32(address, value) - Write an arbitrary 32-bit value at `address`.

    exec(address)           - Execute a function at `address`. We don't need
                              control of any arguments.

To ensure your exploit isn't trash, our server will run your exploit against 5
different builds of the same MuJS code, that we aren't going to give you. All 5
builds are for Linux AARCH64 or X86-64 systems, with reasonable compiler
options. If you write your exploit right, you shouldn't even have to think about
this, it'll "just work" on 64-bit systems.

Notice, you don't need to get arbitrary native code execution, just these three
primitives.


                              What we've given you
                              --------------------
We've given you a modified copy of the MuJS source code in `mujs.zip` and some
scripts so you don't have to deal with any bullshit to test your exploit against
our server. There are no tricks in this challenge. The source code is the MuJS
Git repository, with some staged changes. These staged changes implement
additional features in the engine to make things more fun. Run `git diff HEAD`
to check out the changes from standard MuJS.


                                    The bug
                                    -------
There's a bug in the `Ap_join` function in `jsarray.c`. You figure out the rest
;).


                                Testing locally
                                ---------------
The `run-local.sh` script shows how to test locally. Make sure you're doing this
on a 64-bit system and building a 64-bit build. We've given you a template
`exploit.js` showing what you need to implement. Read the code if curious how it
works.


                                 Building MuJS
                                 -------------
On Ubuntu 20.04, you'll need the following packages:
    apt install cmake libbsd0 libbsd-dev

Then run the `build-mujs.sh` script which will unzip the `mujs.zip` repository
if it hasn't been extracted already, and build the code.


                                Testing remotely
                                ----------------
When you think you've got a working exploit, it's time to test remotely. The
`run-remote.py` will test your exploit against our server. The script POSTs your
exploit script to '<our server>/go'. Our server runs the script against 5
different builds with a maximum timeout of 5 seconds each, and then returns you
a JSON blob with the `stderr` and `stdout` of each run. Each binary is run in a
chroot with a 'flag.txt', which your exploit will print if you implement the
primitives and follow the template. Each 'flag.txt' is a fifth of the flag, and
the flag is all five of them concatenated together. The `run-remote.py` script
will do this for you.

Here is a sample of the expected output of the script:
--------------------------------------------------------------------------------
Result from run against mujs-0 binary:
stdout:
flag{

stderr:


Result from run against mujs-1 binary:
stdout:
FLAG

stderr:


Result from run against mujs-2 binary:
stdout:
WILL

stderr:


Result from run against mujs-3 binary:
stdout:
BE H

stderr:


Result from run against mujs-4 binary:
stdout:
ERE}

stderr:


Maybe flag: flag{FLAG WILL BE HERE}
--------------------------------------------------------------------------------

To reiterate, you shouldn't need to leak back the binaries or anything crazy. If
your exploit doesn't rely on binary offsets, it should work the same on all of
these builds.
