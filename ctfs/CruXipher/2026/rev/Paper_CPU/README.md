rev vm bytecode
A fictional 8-bit CPU with three registers (R0, R1, R2) and 256 bytes of RAM. Programs are raw bytecode. Example binaries and I/O pairs are in the attachment; see README.md for the machine rules and what to run for the flag.


A fictional 8-bit CPU with three registers (**R0**, **R1**, **R2**) and **256 bytes of RAM** (addresses `0x00`–`0xff`).
Before the first instruction: **R0** = input byte, **R1** = **R2** = **0**, **RAM** = all zeros.

Programs are **raw bytecode** (binary files).

**Examples**

Each row: **program** (`examples/*.bin`) + **input** (hex) → **output** (hex).

For examples only, **output** means the value in **R0** when the machine stops.

| Program | In | Out |
|---------|-----|-----|
| `examples/kront.bin` | `2a` | `4a` |
| `examples/vexx.bin` | `00` | `00` |
| `examples/vexx.bin` | `01` | `c3` |
| `examples/blip.bin` | `2a` | `7e` |
| `examples/snok.bin` | `ff` | `55` |

**Challenge**

1. Run `challenge.bin` with input **`2a`** (hex).
2. After the machine stops, read `RAM[0x40]`, `RAM[0x41]`, `RAM[0x42]`, and `RAM[0x43]`.
3. Submit `cruXipher{xxxxxxxx}` where `xxxxxxxx` is those four bytes in order, as **eight lowercase hex digits** (no `0x`, no separators).
