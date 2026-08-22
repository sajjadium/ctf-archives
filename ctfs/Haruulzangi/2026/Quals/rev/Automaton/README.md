by xyptonize
Reverse Engineering
A counterpart agent guards its channel with a gate: hand it the right token and it opens, hand it anything else and it stays shut. The gate does not compare your token to a stored string — it runs your token through a little machine of its own and checks the result. The machine, and what it checks against, are all that ship.

Recover the token the gate will accept. That is your flag.

The handout is a self-contained WebAssembly module (plus a tiny runner); there is no network, no anti-debug, and no trick — the whole answer is deterministically inside it.
