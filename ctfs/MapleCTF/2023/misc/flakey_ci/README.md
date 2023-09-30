nix

We recently deployed a new CI system with Nix, but it seems a little flakey, and has been a bit of a special snowflake of a service. Perhaps one might even say it's a little bit rooted.

But don't worry, we run the builds unprivileged and sandboxed! There is no way you could root our CI box and steal our /flag.


# flakey-ci

## run (vm; easier)

```
nix run .#nixosConfigurations.boxMicro.config.microvm.declaredRunner
nc localhost 1337
```

## run (docker)

```
nix run .#dockerImage.copyToDockerDaemon
docker run --rm --device=/dev/kvm -p 1337:1337 flakey-ci
nc localhost 1337
```
