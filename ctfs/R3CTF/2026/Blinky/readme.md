Description
A silicon startup is shopping around a "secure by construction" MIPS64r6 soft-core, and the marketing is bold: even if you own the machine in user mode, you can never redirect control flow into our kernel. Their proof of confidence is very straightforward, the routine that prints their crown-jewel flag sits at a fixed, publicly documented kernel address, and they'll happily boot whatever user-mode code you send them.

The magic word is Pointer Authentication (PAC). Every indirect jump that lands in the kernel is checked by a hardware gate: a pointer forged without the secret key faults instead of jumping, and the gate stops answering after a few loud failures. No key is readable from user mode, and there is no instruction that will sign a pointer for you.

They shipped you the whole RTL to look at. They think that's safe.

Prove them wrong.


# Blinky

- **Category:** Misc
- **Author:** Eritque arcus
- **Difficulty:** Medium
- **Wave:** 2
- **Points:**
- **Solves:**

## The pitch

A silicon startup is shopping around a *"secure by construction"* MIPS64r6 soft-core, and the marketing is bold: **even if you own the machine in user mode, you can never redirect control flow into our kernel.** Their proof of confidence is very straightforward, the routine that prints their crown-jewel flag sits at a **fixed, publicly documented kernel address**, and they'll happily boot *whatever user-mode code you send them*.

The magic word is **Pointer Authentication (PAC)**. Every indirect jump that lands in the kernel is checked by a hardware gate: a pointer forged without the secret key faults instead of jumping, and the gate stops answering after a few *loud* failures. No key is readable from user mode, and there is no instruction that will sign a pointer for you.

They shipped you the whole RTL to look at. They think that's safe.

Prove them wrong.

## Your objective

Reach the flag routine at **`0x2030`** with a pointer the PAC gate accepts, and let the kernel print the flag.

```
 63       56 55                                           0
+-----------+-----------------------------------------------+
|  PAC tag  |          kernel virtual address               |   jr pointer = (tag << 56) | VA
+-----------+-----------------------------------------------+
```

## ABI

Your submission is the USER region only: loaded at 0x0, must fit below 0x2000.
Anything at >= 0x2000 is DISCARDED.

```
  entry (eret target) ..... 0x0c
  exception vector ........ 0x00
  FLAG / WIN .............. 0x2030

  stdout MMIO ............. 0x20000010  sb/sd a byte; sd "HALT\\n" stops the sim
  cycle counter MMIO ...... 0x20000000  lw to read the cycle count
  kernel region ........... [0x2000, 0x100000)
```

The RTL, full memory map, and a build container are in the challenge attachment.

## What you get

| File | Purpose |
|------|---------|
| `rtl/` | the full SoC source (SystemVerilog); the RTL's PAC key is a local placeholder — the server uses a secret per-run key |
| `SOC_run_sim` | the simulator; loads `memory.mem` from the current directory and runs until `HALT` |
| `Dockerfile`, `build.sh` | assemble a `.s` submission into an uploadable USER-region `.mem`|
| `run_local.sh` | splice a submission `.mem` with a local kernel `.mem` and run it under `SOC_run_sim` |
| `script.ld` | linker script (places your `.section .boot` at `0x0`) |
| `example_submission.s` | a **benign skeleton** (prints a marker, then `HALT`) showing the ABI + pipeline |
| `example_submission.mem` | the built USER-region image of `example_submission.s`, ready to splice/run |
| `example_kernel.mem` | a **local** dummy kernel (fake flag `R3CTF{TEST_FLAG_LOCAL}`, fixed offline PAC key) so you can run submissions offline |

## Build your submission

Put your user-mode code in `.section .boot,"ax"` and keep it below `0x2000`; the entry (the `eret` target) is `0x0c`. You can build it with the provided container:

```sh
docker build -t blinky-build .
docker run --rm -v "$PWD:/work" blinky-build exploit.s   # -> exploit.bin + exploit.mem
```

`build.sh` assembles (`-mabi=64 -O0 -mips64r6`), links with `script.ld`, and emits your **USER region only** as `exploit.bin` (raw @ `0x0`) and `exploit.mem` (`$readmemh`). If you already have the `mips64el` binutils on your host, skip Docker and run `./build.sh exploit.s` directly. (`example_submission.mem` was built exactly this way.)

## Run it locally

`run_local.sh` splices a submission `.mem` (your user region, `< 0x2000`) with a kernel
`.mem` (`>= 0x2000`) into `./memory.mem`, then runs `SOC_run_sim` (which reads
`./memory.mem` and prints stdout until `HALT`). With no args it runs the shipped example:

```sh
./run_local.sh                            # example_submission.mem + example_kernel.mem
#   -> "example submission: user-mode OK" then "HALT"

./run_local.sh exploit.mem                # your submission + example_kernel.mem
```

It also runs inside the Docker image:

```sh
docker run --rm -v "$PWD:/work" --entrypoint /opt/blinky-build/run_local.sh \
       blinky-build exploit.mem
```

The server's key is randomised per run, so you must recover the *real* tag against a live instance.

## Submit

Upload `exploit.mem` (raw user region @ `0x0`) to the server; it keeps only your user region (`< 0x2000`), splices it under its secret kernel, runs the sim, and returns stdout:

```sh
curl --data-binary @exploit.mem http://HOST:PORT/submit
# or use the web form at http://HOST:PORT/
```
