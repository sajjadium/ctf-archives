# Revenge of Pwn

## How This Challenge Work

`exploit.py` is able to exploit `chal/vuln`.

```
exploit.py --- pwn --->   chal/vuln
                       127.0.0.1:1337
```

Now you have the chance to *replace* the binary listening on 1337 port,
and you need to pwn the script who is pwning your binary!

```
exploit.py --- (will try to) pwn --->  <your uploaded file>
    ^                                     127.0.0.1:1337
    |
    |
you need to pwn this
```

The flag is located at `/home/deploy/flag`, which is readable by `exploit.py`.
