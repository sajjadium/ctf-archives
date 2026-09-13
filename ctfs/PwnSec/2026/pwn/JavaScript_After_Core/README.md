javascript-after-core.md
We pinned JavaScriptCore to a WebKit revision from just before a certain fix landed, stripped every convenience the jsc shell hands a would-be exploiter, and bolted a single door onto it.

win(str, callback) is that door. It takes the string hello!!! and your callback, and calls the callback twice. Between the two calls the string must read pwned!!!; after the second it must read world!!!. Strings in JavaScript are immutable, so the language says this is impossible. Do it anyway and the server prints the flag.

What is left in the shell: print, quit, gc, fullGC, edenGC, gcHeapSize. What is gone: addressOf, describe, describeArray, read, readFile, write, load, run, runString, createGlobalObject, createNonRopeNonAtomString, transferArrayBuffer, jscOptions, $ and $262. No debug build, no JIT flags, no leaked addresses.

Send one JavaScript program. It runs once, then the connection closes.

The archive contains the exact patch applied to the shell, the pinned revision, and the Dockerfile that builds it, so you can reproduce the target locally. It is x86-64.

@m411k
