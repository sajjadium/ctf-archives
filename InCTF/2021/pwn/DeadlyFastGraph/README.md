# DeadlyFastGraph

The given patch applies to commit `c40e806df2c49dac3049825cf48251a230296c6e` on the WebKit git repository.

The release build running remote was built on `Ubuntu 18.04`, and it is running with the flag `--useConcurrentJIT=false`.

Run `/readflag` on the server once you get a shell to retrieve your flag.

## Build Instructions (Debug)

```sh
git clone https://github.com/WebKit/WebKit.git
cd WebKit
git checkout c40e806df2c49dac3049825cf48251a230296c6e
patch -p1 < dfg.patch
Tools/Scripts/build-webkit --jsc-only --debug
cd WebKitBuild/Debug/bin

./jsc --useConcurrentJIT=false
```