by Hidden Investigations
Miscellaneous
A hobbyist had a quiet obsession: figuring out, without asking anyone, which unknown place they kept drifting back to on autopilot. Their idea was to mine two signals their phone already recorded — step-count spikes and the strength of nearby Wi-Fi access points — on the theory that a place that truly matters shows up as you moving around near the same access point, over and over.

They never finished it. All that's left is a handful of files pulled off the old project folder: some scratch notes, a tiny config, one exported scan, and the log of the single run that actually worked.

No server, no service, nothing to connect to. This is pure offline forensics. Reconstruct the person's scoring rule from what the files imply — the movement cutoff that separates "walking" from "sitting still", and how a per-access-point score is built from signal strength and the trust weights — then apply it to the full export and name the place they kept returning to. The loudest access point is a trap; so is the one that appears most often. Get the rule right and exactly one place rises to the top.

The derived place name is the key to the flag. Submit it as hiCTF{PlaceName}, with the name spelled as the access point appears in the files.
