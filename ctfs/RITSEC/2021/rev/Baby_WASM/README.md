This is a JS engine pwn challenge.

V8 version: 8.7.220

V8 commit: 0d81cd72688512abcbe1601015baee390c484a6a

glibc version: 2.31

OS: Ubuntu 20.04.2 - 64 bit

Provided challenge files: V8 debug and release builds, diff and patch files, challenge setup files, libc.so.6

The server will be running the release build.

Note: My intended solution is not only about 90% reliable so if you are sure it has worked locally, in debug or release, but cannot get it to work remotely, please try to run your exploit many more times. Please talk to me if you think there is an issue.

Give us a link to your exploit and we will run it like ./d8 <file.js>

Note: If you execute /bin/sh the runner will try to print flag for you. If you go any other ways and it works locally but not remotely, please talk to me.

If you have a working exploit locally for babywasm but it does not work remotely when you give the URL, and if you host it from your own server, your server might have blocked our server from downloading it, most likely due to user-agent string. So please find somewhere public like pastebin and post it there unlisted to try again. Thank you!

nc challenges1.ritsec.club 1337

Download Link: https://drive.google.com/file/d/11OSPsOZY_MwarKDeaLNCsilSiD-70ztq/view?usp=sharing
