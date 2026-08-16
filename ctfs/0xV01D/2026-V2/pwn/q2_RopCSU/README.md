wave2 pwn hard
0x4sh

q2 — RopCSU (pwn)
Port	20002
Points (suggested)	250
Files	chall, libc.so.6
Difficulty	Hard
EN: No win(). No leaks. The binary only offers puts and read. The libc is in your hands — you just have to find it at runtime. The __libc_csu_init gadgets are waiting to call anything you point them at. Two-stage: leak, then land.

AR: ما في win(). ما في أي تسريب. الباينري ما يعطيك غير puts و read. الـ libc بين إيديك — بس لازم تلقاه وقت التشغيل. كيدجيتات __libc_csu_init مستنية أي شي توجّهها له. مرحلتين: تسريب، ثم إصابة.

chall — 64-bit ELF (NX, no PIE, no canary)
libc.so.6 — glibc 2.39 (the exact one on the server)
