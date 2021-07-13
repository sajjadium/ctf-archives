In this challenge, you will attempt to escape the Chrome sandbox on Linux and achieve control of the Browser process.
Setup

You are provided with a modified Chrome version, with an added vulnerability and several utilities to simulate a compromised renderer process.

The vulnerability is in a new mojo interface named Hack, which allows the renderer to allocate and free regions of memory, and read from them. However, reads are not bound-checked, allowing for information disclosure. The interface is described in hack.mojom as:

interface Hack {
    Allocate(uint64 size) => (uint64 id);
    Free(uint64 id) => ();
    Read(uint64 id, uint64 offset, uint64 size) => 
        (array<uint8> bytes);
}

An exampletory use of this vulnerability, using MojoJS:

var hack_ptr = new blink.mojom.HackPtr();
Mojo.bindInterface(blink.mojom.Hack.name, mojo.makeRequest(hack_ptr).handle)

async function foo() {
    let allocation = await hack_ptr.allocate(10);
    data = await hack_ptr.read(allocation.id, 100, 10);
    console.log(data.bytes); // Will print 10 bytes from offset 100 of the allocation
}
foo();

In addition, to simulate control of the renderer, the following utilities are available:

    getaddress(object) - takes a single argument that is an object, and returns its address as a BigInt
    readwrite(BigInt base) - returns a large ArrayBuffer, whose data is at address base.
    callforeign(BigInt function_address, BigInt arg1, ...) - calls a native function at function_address with arguments arg1, ... (up to 4 arguments). The return value of the function is returned as a BigInt.
    dlopen(string library_name) - Gets the address of a loaded library. The returned BigInt may be passed as a handle to dlsym. Note that the sandbox will not allow loading a library that is not already loaded. To help you load your own library, dlopen("./libhack.so", RTLD_NOW) is executed before the sandbox is initialized, so you may use dlopen("./libhack.so") in JS to access your own library.
    dlsym(BigInt handle, string symbol_name) - Get the address of a symbol as a BigInt.
    MojoJS is enabled by default.

Allowed modifications

In addition to the utilities listed above, you may choose to introduce additional patches to Chrome to aid in exploitation, as long as they affect the renderer process only.
Success Criteria

To win the challenge, you must demonstrate complete control of the browser process by executing arbitrary code. You may also submit partial solutions that achieve some exploit capability short of full control (such as a limited write capability, or a UaF). If no winner is selected, a partial score may be awarded for a partial solution.

Solutions will be judged on Ubuntu 18.04, and must achieve the desired result with reliability > 51%.

Your solution must be based on novel research. In particular, do not use recently fixed security issues that may not be fixed in the challenge Chrome version.
Submission

A submission should include any code used in the exploit:

    HTML/JS files
    Source code for libhack.so if used
    Any additional renderer patches

General Narrative

The point of this challenge is to prove the probability of exploiting an info-leak. We hope you guys show good spirit and intentions :)
Package

To make it easier for you to win this challenge we have precompiled everything and are providing everything in a file (6GB): (deprecated, use new link) https://typhooncon.s3.us-east-2.amazonaws.com/Chrome+Compilation.zip

Updated link: https://typhooncon.s3.us-east-2.amazonaws.com/New+Chrome+Compilation.zip
