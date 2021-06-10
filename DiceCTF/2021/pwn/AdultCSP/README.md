I've decided to a bit of dev work on my chrome instance. I'm not sure if it's very secure though, can you give it a look?

Some relevant files:

`~/chromium/src (ctf) $ git log -10 > log.txt`

`~/chromium/src (ctf) $ git diff 36207b9a431a90704bec616b9f6b972ec85db777 72ef15b02c86efcf5c4a0c7b1134bcbb928143f6 > diff.txt`

```
~/chromium/src (ctf) $ cat out/Default/args.gn
# Set build arguments here. See `gn help buildargs`.
is_debug=false
```

```
~/chromium/src (ctf) $ sha1sum out/Default/chrome
a941d8692603dba7c75bb1330cc25b04e2882faa  out/Default/chrome
```

<a href="https://chromium.googlesource.com/chromium/src/+/master/docs/linux/build_instructions.md">Setting up a Build</a>

<a href="https://dicegang.storage.googleapis.com/babier-csp/chromium-k0r4k2jinmr3e8dxjjf6he6ckcpqloo0.tar.gz">Deployment Files</a>

To run:
```
./chromium/chrome --enable-blink-features=MojoJS --user-data-dir=/does-not-exist --headless --disable-gpu --remote-debugging-port=9222 $URL
```

<a href="https://us-east1-dicegang.cloudfunctions.net/ctf-2021-babier-csp?challenge=babier-csp">Admin Bot</a>

The admin bot has a timeout of 20 seconds. The reference solution runs in around 10 seconds against remote.

The flag is stored at `./flag-$(openssl rand -hex 16)`
