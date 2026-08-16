wave2 pwn very-hard
0x4sh

q3 — The Vault (pwn)
Port	20003
Points (suggested)	400
Files	chall, libc.so.6
Difficulty	Very Hard
EN: Every mitigation is on: canary, PIE, full RELRO, NX. One careless printf(buf) gives you a single format-string round. Use it to carve out the canary, the PIE, and the libc from the stack — then one more gift overflows into a ROP chain. The vault opens from the inside.

AR: كل الحمايات مفعلة: canary، PIE، Full RELRO، NX. printf(buf) وحدة متهورة تعطيك جولة format string واحدة. استخدمها لتقتطع الـ canary والـ PIE والـ libc من الـ stack — وبعدها هدية ثانية تفيض وتزرع ROP chain. الخزنة بتفتح من جوّا.

chall — 64-bit ELF (NX, PIE, canary, FULL RELRO)
libc.so.6 — glibc 2.39 (the exact one on the server)
