wave2 pwn medium
0x4sh

q1 — Shellgame (pwn)
Port	20001
Points (suggested)	100
Files	chall
Difficulty	Medium
EN: The gatekeeper of V0ID only opens for a very specific pair of gifts: 0xdeadbeef and 0xcafebabe. Overflow the guard's stack and hand them over in exactly the right order. There is a win() that will drop you a shell — but it needs arguments.

AR: حارس البوابة ما بيفتح إلا بهدية محددة: 0xdeadbeef و 0xcafebabe. افعل الفيضان على الـ stack وسلمه الهدايا بالترتيب الصحيح — في دالة win() بتعطيك شيل، بس محتاجة وسائط.

chall — 64-bit ELF (NX, no PIE, no canary)
