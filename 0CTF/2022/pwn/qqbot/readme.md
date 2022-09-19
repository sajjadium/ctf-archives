you can setup your private server with following command:

```
apt install prosody
service start prosody
prosodyctl adduser test@localhost
```

and run your bot like:
```
apt install libotr5 libstrophe0
./qqbot <account> <pass> <host>
```