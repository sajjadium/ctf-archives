## Setup

Nightmare is an extremely environment sensitive challenge. It's important your environment is as accurate as possible.
Tools such as patchelf will clobber continuity between local and remote. Please take care making changes.

You might have noticed that no libc was shipped with this challenge. This is intentional. Please do NOT try to exploit
the binary outside of the provided Docker and utilize the libc and ld within the docker.

You are safe to install tools and other items in the docker. The docker tag is `ubuntu@sha256:cc8f713078bfddfe9ace41e29eb73298f52b2c958ccacd1b376b9378e20906ef`.

### Symbols

You can install debug symbols by installing libc6-dbg package. From there, please do NOT unstrip the global libc and ld.
Make a copy and unstrip them without affecting /usr/lib. An unstripping script is provided.

## Remote

Nightmare's remote requires you to submit a static payload to the program. This payload will then be sent to 8 different instances of Nightmare, all of which have `stdout` hidden from the competitor. This prevents leaking ASLR base and bruteforce. In order to submit a payload, simply:

- Send the size of the payload packed as a 8 byte integer
- Send the payload

## Security Measures

The seccomp used can be found in `bin/filter.s`.
