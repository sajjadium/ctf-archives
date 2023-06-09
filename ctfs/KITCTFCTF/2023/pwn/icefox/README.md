My browser is so slow lately that I just had to do something about it. All I had to do was remove a few lines of code resulting in a 50% speedup on the benchmark I ran. No idea what those firefox devs are doing, but with icefox you can finally enjoy browsing in light speed!


# deploy/
* Contains the remote setup
* Before being able to deploy this locally, you need to download the given firefox js-shell binary
    * Place the downloaded js.tar.gz in deploy/ and extract it

# build/
* Contains the firefox patch that should apply cleanly to revision ``eaba732ce0ab``
* To build the firefox js shell on your own you can follow the [Building Firefox On Linux instructions](https://firefox-source-docs.mozilla.org/setup/linux_build.html)
* Also make sure to checkout the correct revision with ``hg update eaba732ce0ab``, apply the patch with ``hg import --no-commit patch.diff`` and use the following mozconfig
```
ac_add_options --enable-project=js

ac_add_options --disable-debug
ac_add_options --enable-optimize

mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/jsshell
```
* After the build is complete you should find the actually js binary at jsshell/dist/bin/js
