type this, type that, I just can't take it anymore. 6 years passed and I am still too stupid to exploit this bug. So, instead of suffering much longer, I let my friend do it for me. He actually got it to work. Can you prove yourself as well?
The only thing I figured out himself is that js-call-reducer.cc does look a little bit sus...


# deploy/
    * Contains the remote setup
    * Before being able to deploy this locally, you need to download the given compiled chromium (http://ctf.ju256.de/d08465b26f560787d789bb57d58d5c4fd5fd9caf4a502844e612d7655512b663/chrome.tar.gz)!
        * Place the downloaded chrome.tar.gz in deploy/ and extract it (The extracted version is about 13GB. So make sure you have enough space so you don't repeatedly fill up your disk like me!)
    * For every submitted URL an individual container is spawned
    * The container gets 8GB of RAM and 2 CPUs

# build/
    * Contains the v8 patch that should apply cleanly to the latest chromium linux stable (113.0.5672.126) / v8 release 113.0.5672.126 (as of 31.05.2023)
    * The given chromium was built with the following args.gn and with the v8 patch applied:
    ```
    is_debug = false
    dcheck_always_on = false
    symbol_level = 2
    ```
    * To get a local debug version of the V8 developer shell (d8) you can follow the build instructions [here](https://v8.dev/docs/build)
        * Don't forget to apply the patch before running ``tools/dev/gm.py x64.release`` / ``tools/dev/gm.py x64.debug``
