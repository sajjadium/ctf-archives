## Ateles

This directory only contains the patch file. For the entire environment with the built browser/js_shell, please download the `ateles_handout_large.zip` file.

### Submitting your exploit

Once you test your exploit locally and ensure that it works, you have to upload your exploit online. You can then nc to our server (ip/port on the ctf page) where you will be prompted to give a link to your exploit.

We will then run the vulnerable firefox and open the URL that you sent us. We will wait for 10 seconds after this and at the end of the 10 seconds, if there is a `/usr/bin/xcalc` on running in the Docker container, we print out the flag. Else we will print out `Failed`.

### Build instructions

Although both, the built firefox and a built non-debug js shell have been provided in `ateles_handout_large.zip`, here are the build suggestions in case you still want to compile your own js_shell/ browser.

```sh
# grab the code
hg clone http://hg.mozilla.org/mozilla-central spidermonkey

# move the patch file into the cloned source
mv patch.diff spidermonkey && cd spidermonkey

# apply the patch
patch -p1 < patch.dif
```

For building a js_shell

```sh

cd js/src/
cp configure.in configure && autoconf2.13
mkdir build_debug.obj && cd build_debug.obj

# Configuring a debug build.
# For non-debug, switch the `--enable-debug` with `--disable-debug`
../configure --enable-debug --enable-optimize --enable-ion

make -j4

cd dist/bin/
```

Please run the js_shell with `--no-threads` and `--ion-offthread-compile=off` to make your exploits realiable.

```sh
./js --no-threads --ion-offthread-compile=off
```

Even on the remote server, `ion-offthread-compile` is set to false and sandbox is disabled.

For building the entire browser

```sh

cd spidermonkey

cat > mozconfig<<EOF
mk_add_options MOZ_OBJDIR=./intctf_ateles
EOF

./mach build
```
The built browser will be present in `spidermonkey/intctf_ateles/dist/bin/firefox`

Enjoy!
