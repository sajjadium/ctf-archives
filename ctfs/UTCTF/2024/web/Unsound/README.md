I decided to roll my own super secure crypto. It's also written in Rust with no unsafe code. If you get past all of that, you have to break through the Wasm sandbox. Good luck...you'll need it.

All web requests replayed on an internal headless browser, which contains the flag. This is necessary since any keys stored in Javascript / Wasm could easily be read by the attacker. Take this into account when attacking this box.

By Aadhithya (@aadhi0319 on discord)
