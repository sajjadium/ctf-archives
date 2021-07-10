This is a two part challenge. 

The first part is intended to be a baby challenge, and the challenge environment will have the `CTF_CHALLENGE_EASY_MODE` environment variable set. For an introduction to SBX, see [this post](https://robertchen.cc/blog/2021/07/07/sbx-intro.html). 

Note that this challenge was designed to be solvable without setting up your own Chromium build. However, the build data is still provided for completeness. 

```
$ cat out/pwn/args.gn
is_debug=false
$ git diff HEAD~1 HEAD > ~/ctf-challenge/diff
$ git log -n 3 > ~/ctf-challenge/log
```

To run: 
```
./chromium/chrome --enable-blink-features=MojoJS --user-data-dir=/does-not-exist --headless --disable-gpu --remote-debugging-port=$((1024 + $RANDOM % 10000)) $PAYLOAD_URL
```

The actual admin bot is run with [redpwn/admin-bot](https://github.com/redpwn/admin-bot). 

Once you have a shell, the flag is located at `/flag-random-string-here`.
