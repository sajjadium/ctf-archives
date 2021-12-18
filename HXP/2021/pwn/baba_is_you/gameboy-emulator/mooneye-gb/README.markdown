# Mooneye GB

Mooneye GB is a Game Boy research project and emulator written in Rust.

[![Build Status](https://github.com/Gekkio/mooneye-gb/workflows/ci/badge.svg)](https://github.com/Gekkio/mooneye-gb/actions)

The main goals of this project are accuracy and documentation. Some existing
emulators are very accurate (Gambatte, BGB >= 1.5) but are not documented very
clearly, so they are not that good references for emulator developers. I want
this project to document as clearly as possible *why* certain behaviour is
emulated in a certain way. This also means writing a lot of test ROMs to figure
out corner cases and precise behaviour on real hardware.

For documentation about known behaviour, see [Game Boy: Complete Technical
Reference](https://github.com/Gekkio/gb-ctr)

[Binary test ROMs are available here](https://gekkio.fi/files/mooneye-gb/latest/)
in a zip package and also as individual .gb files. They are automatically
built and deployed whenever there's new changes in the master branch.

Non-goals:

* CGB (Game Boy Color) support. It would be nice, but I want to make the normal
  Game Boy support extremely robust first.
* A debugger
* A good user interface. Building native UIs with Rust is a bit painful at the
  moment.

**Warning**:

* Project is WIP
* Doesn't work properly without a boot ROM
* The emulator is lagging behind hardware research. I don't want to spend time
  making short-lived and probably incorrect fixes to the emulator if I'm not
  sure about the hardware behaviour.

## Hardware testing

There's tons of documentation and tons of emulators in the internet, but in the
end I only trust real hardware. I follow a fairly "scientific" process when
developing emulation for a feature:

1. Think of different ways how it might behave on real hardware
2. Make a hypothesis based on the most probable behaviour
3. Write a test ROM for such behaviour
4. Run the test ROM on real hardware. If the test ROM made an invalid
   hypothesis, go back to 1.
5. Replicate the behaviour in the emulator

All test ROMs are manually run with these devices:

| Device              | Model    | Mainboard    | CPU              | Detailed information                                                            |
| ------------------- | -------- | ------------ | ---------------- | ---------------                                                                 |
| Game Boy            | DMG-01   | DMG-CPU-01   | DMG-CPU          | [G01176542](https://gbhwdb.gekkio.fi/consoles/dmg/G01176542.html)               |
| Game Boy            | DMG-01   | DMG-CPU-02   | DMG-CPU A        | [G02487032](https://gbhwdb.gekkio.fi/consoles/dmg/G02487032.html)               |
| Game Boy            | DMG-01   | DMG-CPU-04   | DMG-CPU B        | [G10888299](https://gbhwdb.gekkio.fi/consoles/dmg/G10888299.html)               |
| Game Boy            | DMG-01   | DMG-CPU-06   | DMG-CPU C        | [GM6058180](https://gbhwdb.gekkio.fi/consoles/dmg/GM6058180.html)               |
| Super Game Boy      | SHVC-027 | SGB-R-10     | SGB-CPU-01       | [SGB Unit #2 \[gekkio\]](https://gbhwdb.gekkio.fi/consoles/sgb/gekkio-2.html)   |
| Game Boy Pocket     | MGB-001  | MGB-CPU-01   | CPU MGB          | [M10280516](https://gbhwdb.gekkio.fi/consoles/mgb/M10280516.html)               |
| Super Game Boy 2    | SHVC-042 | SHVC-SGB2-01 | CPU SGB2         | [SGB2 Unit #1 \[gekkio\]](https://gbhwdb.gekkio.fi/consoles/sgb2/gekkio-1.html) |
| Game Boy Color      | CGB-001  | CGB-CPU-01   | CPU CGB          | [C10203977](https://gbhwdb.gekkio.fi/consoles/cgb/C10203977.html)               |
| Game Boy Color      | CGB-001  | CGB-CPU-01   | CPU CGB A        | [C10400331](https://gbhwdb.gekkio.fi/consoles/cgb/C10400331.html)               |
| Game Boy Color      | CGB-001  | CGB-CPU-02   | CPU CGB B        | [C11778414](https://gbhwdb.gekkio.fi/consoles/cgb/C11778414.html)               |
| Game Boy Color      | CGB-001  | CGB-CPU-03   | CPU CGB C        | [CGB Unit #1 \[gekkio\]](https://gbhwdb.gekkio.fi/consoles/cgb/gekkio-1.html)   |
| Game Boy Color      | CGB-001  | CGB-CPU-05   | CPU CGB D        | [CH20983903](https://gbhwdb.gekkio.fi/consoles/cgb/CH20983903.html)             |
| Game Boy Color      | CGB-001  | CGB-CPU-06   | CPU CGB E        | [CH24224683](https://gbhwdb.gekkio.fi/consoles/cgb/CH24224683.html)             |
| Game Boy Advance    | AGB-001  | AGB-CPU-01   | CPU AGB          | [AH10045235](https://gbhwdb.gekkio.fi/consoles/agb/AH10045235.html)             |
| Game Boy Advance    | AGB-001  | AGB-CPU-10   | CPU AGB A        | [AH12465671](https://gbhwdb.gekkio.fi/consoles/agb/AH12465671.html)             |
| Game Boy Player     | DOL-017  | DOL-GBS-20   | CPU AGB A E      | [GBS Unit #3 \[gekkio\]](https://gbhwdb.gekkio.fi/consoles/gbs/gekkio-3.html) |
| Game Boy Advance SP | AGS-001  | C/AGS-CPU-01 | CPU AGB B        | [XJH10027945](https://gbhwdb.gekkio.fi/consoles/ags/XJH10027945.html)           |
| Game Boy Advance SP | AGS-001  | C/AGS-CPU-21 | CPU AGB B E      | [XEH17807928](https://gbhwdb.gekkio.fi/consoles/ags/XEH17807928.html)           |

### Additional devices

I also have access to more devices with different mainboard revisions, but I
think the CPU revision is all that matters if we study the behaviour and not
analog characteristics (e.g. audio filtering). Even if audio sounded different
between two units with the same CPU revision but different mainboard revisions,
I'd expect the difference to be caused by individual device variation or
different revisions of support chips (e.g. RAM/AMP/REG).

The main "test fleet" is already very big, so I will only use these devices if
there's evidence of behaviour that depends on mainboard revision or individual
units.

| Device              | Model    | Mainboard    | CPU              | Detailed information                                                          |
| ------------------- | -------- | ------------ | -----------      | ----                                                                          |
| Game Boy            | DMG-01   | DMG-CPU-01   | DMG-CPU          | [G01036814](https://gbhwdb.gekkio.fi/consoles/dmg/G01036814.html)             |
| Game Boy            | DMG-01   | DMG-CPU-03   | DMG-CPU B        | [G06551776](https://gbhwdb.gekkio.fi/consoles/dmg/G06551776.html)             |
| Game Boy            | DMG-01   | DMG-CPU-05   | DMG-CPU B        | [G13289095](https://gbhwdb.gekkio.fi/consoles/dmg/G13289095.html)             |
| Game Boy            | DMG-01   | DMG-CPU-06   | DMG-CPU B        |                                                                               |
| Game Boy            | DMG-01   | DMG-CPU-07   | DMG-CPU B (blob) | [G38953646](https://gbhwdb.gekkio.fi/consoles/dmg/G38953646.html)             |
| Game Boy            | DMG-01   | DMG-CPU-08   | DMG-CPU C (blob) |                                                                               |
| Super Game Boy      | SNSP-027 | SGB-R-10     | SGB-CPU-01       | [SGB Unit #7 \[gekkio\]](https://gbhwdb.gekkio.fi/consoles/sgb/gekkio-7.html) |
| Game Boy Pocket     | MGB-001  | MGB-ECPU-01  | CPU MGB          | [MH12573718](https://gbhwdb.gekkio.fi/consoles/mgb/MH12573718.html)           |
| Game Boy Pocket     | MGB-001  | MGB-LCPU-01  | CPU MGB          | [M12827347](https://gbhwdb.gekkio.fi/consoles/mgb/M12827347.html)             |
| Game Boy Pocket     | MGB-001  | MGB-LCPU-02  | CPU MGB          | [MH20284468](https://gbhwdb.gekkio.fi/consoles/mgb/MH20284468.html)           |
| Game Boy Light      | MGB-101  | MGL-CPU-01   | CPU MGB          | [L10610653](https://gbhwdb.gekkio.fi/consoles/mgl/L10610653.html)             |
| Game Boy Color      | CGB-001  | CGB-CPU-04   | CPU CGB D        | [C19220030](https://gbhwdb.gekkio.fi/consoles/cgb/C19220030.html)             |
| Game Boy Advance    | AGB-001  | AGB-CPU-02   | CPU AGB          | [AJ12569062](https://gbhwdb.gekkio.fi/consoles/agb/AJ12569065.html)           |
| Game Boy Advance    | AGB-001  | AGB-CPU-03   | CPU AGB A        | [AJ14804298](https://gbhwdb.gekkio.fi/consoles/agb/AJ14804298.html)           |
| Game Boy Advance    | AGB-001  | AGB-CPU-04   | CPU AGB A        | [AJ15529163](https://gbhwdb.gekkio.fi/consoles/agb/AJ15529163.html)           |
| Game Boy Player     | DOL-017  | DOL-GBS-10   | CPU AGB A        | [GBS Unit #1 \[gekkio\]](https://gbhwdb.gekkio.fi/consoles/gbs/gekkio-1.html) |
| Game Boy Advance SP | AGS-001  | C/AGS-CPU-10 | CPU AGB B        | [XEH12776954](https://gbhwdb.gekkio.fi/consoles/ags/XEH12776954.html)         |
| Game Boy Advance SP | AGS-001  | C/AGS-CPU-11 | CPU AGB B        | [XJF10485171](https://gbhwdb.gekkio.fi/consoles/ags/XJF10485171.html)         |
| Game Boy Advance SP | AGS-001  | C/AGS-CPU-30 | CPU AGB B E      | [XEH20137204](https://gbhwdb.gekkio.fi/consoles/ags/XEH20137204.html)         |
| Game Boy Advance SP | AGS-101  | C/AGT-CPU-01 | CPU AGB B E      | [XU72764025-1](https://gbhwdb.gekkio.fi/consoles/ags/XU72764025-1.html)       |

I'm still looking for the following mainboards, but these are probably not
required for reverse engineering:

* SGB-R-01
* SGB-N-01
* SGB-N-10
* C/AGS-CPU-20
* DOL-GBS-01

**For now, the focus is on DMG/MGB/SGB/SGB2 emulation, so not all tests pass on
CGB/AGB/AGS or emulators emulating those devices.**

## Performance

**Always compile in release mode if you care about performance!**

On a i7-3770K desktop machine I can usually run ROMs with 2000 - 4000% speed.
Without optimizations the speed drops to 150 - 200%, which is still fine for
development purposes.

Raspberry Pi with X11 desktop works but is too slow because there is no OpenGL
acceleration.

The emulator is runnable on Android, but cross-compiling and packaging is a
huge pain and touch controls would have to be implemented, so I'm not
supporting Android at the moment.

## Running the emulator

Requirements:

* Rust 1.26
* SDL2 development libraries for your platform must be installed

### GUI

1. `cargo run --release`
2. Follow the instructions

### Command-line
1. Acquire a Game Boy bootrom, and put it to `$HOME/.local/share/mooneye-gb/bootroms/dmg_boot.bin`
2. `cargo build --release`
3. `cargo run --release -- PATH_TO_GAMEBOY_ROM`

On Windows, also download an SDL2 package containing SDL2.dll, and put it to
`target/debug` and `target/release`.

### Game Boy keys

| Game Boy | Key        |
| -------- | ---------- |
| Dpad     | Arrow keys |
| A        | Z          |
| B        | X          |
| Start    | Return     |
| Select   | Backspace  |

### Other keys

| Function                   | Key       |
| -------------------------- | --------- |
| Fast forward               | Shift     |
| Toggle performance overlay | F2        |

## Test suite

### Blargg's tests

| Test              | mooneye-gb |
| ----------------- | ---------- |
| cpu instrs        | :+1:       |
| dmg sound 2       | :x:        |
| instr timing      | :+1:       |
| mem timing 2      | :+1:       |
| oam bug 2         | :x:        |
| cgb sound 2       |            |

Notes:

* cpu_instrs fails on MGB/SGB2 hardware and emulators emulating them correctly.
  The ROM incorrectly detects the device as CGB, and attempts to perform a CPU
  speed change which causes a freeze (STOP instruction with joypad disabled)
* dmg_sound-2 test #10 can fail randomly on real hardware and seems to depend
  on non-deterministic behaviour.
* oam_bug-2 fails on all CGB, AGB, and AGS devices
* cgb_sound-2 test #03 fails on CPU CGB, CPU CGB A, and CPU CGB B

### Mooneye GB acceptance tests

| Test                    | mooneye-gb |
| ----------------------- | ---------- |
| add sp e timing         | :+1:       |
| boot div dmg0           | :x:        |
| boot div dmgABCmgb      | :x:        |
| boot div S              | :x:        |
| boot div2 S             | :x:        |
| boot hwio dmg0          | :x:        |
| boot hwio dmgABCmgb     | :x:        |
| boot hwio S             | :+1:       |
| boot regs dmg0          | :+1:       |
| boot regs dmgABC        | :+1:       |
| boot regs mgb           | :+1:       |
| boot regs sgb           | :+1:       |
| boot regs sgb2          | :+1:       |
| call timing             | :+1:       |
| call timing2            | :+1:       |
| call cc_timing          | :+1:       |
| call cc_timing2         | :+1:       |
| di timing GS            | :+1:       |
| div timing              | :+1:       |
| ei sequence             | :+1:       |
| ei timing               | :+1:       |
| halt ime0 ei            | :+1:       |
| halt ime0 nointr_timing | :+1:       |
| halt ime1 timing        | :+1:       |
| halt ime1 timing2 GS    | :+1:       |
| if ie registers         | :+1:       |
| intr timing             | :+1:       |
| jp timing               | :+1:       |
| jp cc timing            | :+1:       |
| ld hl sp e timing       | :+1:       |
| oam dma_restart         | :+1:       |
| oam dma start           | :+1:       |
| oam dma timing          | :+1:       |
| pop timing              | :+1:       |
| push timing             | :+1:       |
| rapid di ei             | :+1:       |
| ret timing              | :+1:       |
| ret cc timing           | :+1:       |
| reti timing             | :+1:       |
| reti intr timing        | :+1:       |
| rst timing              | :+1:       |

#### Bits (unusable bits in memory and registers)

| Test           | mooneye-gb |
| -------------- | ---------- |
| mem oam        | :+1:       |
| reg f          | :+1:       |
| unused_hwio GS | :+1:       |

#### Instructions

| Test                        | mooneye-gb |
| --------------------------- | ---------- |
| daa                         | :+1:       |

#### Interrupt handling

| Test                        | mooneye-gb |
| --------------------------- | ---------- |
| ie push                     | :+1:       |

#### OAM DMA

| Test                        | mooneye-gb |
| --------------------------- | ---------- |
| basic                       | :+1:       |
| reg_read                    | :+1:       |
| sources GS                  | :+1:       |

#### PPU

| Test                        | mooneye-gb |
| --------------------------- | ---------- |
| hblank ly scx timing GS     | :+1:       |
| intr 1 2 timing GS          | :+1:       |
| intr 2 0 timing             | :+1:       |
| intr 2 mode0 timing         | :+1:       |
| intr 2 mode3 timing         | :+1:       |
| intr 2 oam ok timing        | :+1:       |
| intr 2 mode0 timing sprites | :x:        |
| lcdon timing GS             | :x:        |
| lcdon write timing GS       | :x:        |
| stat irq blocking           | :x:        |
| stat lyc onoff              | :x:        |
| vblank stat intr GS         | :+1:       |

#### Serial

| Test                        | mooneye-gb |
| --------------------------- | ---------- |
| boot sclk align dmgABCmgb   | :x:        |

#### Timer

| Test                 | mooneye-gb |
| -------------------- | ---------- |
| div write            | :+1:       |
| rapid toggle         | :+1:       |
| tim00 div trigger    | :+1:       |
| tim00                | :+1:       |
| tim01 div trigger    | :+1:       |
| tim01                | :+1:       |
| tim10 div trigger    | :+1:       |
| tim10                | :+1:       |
| tim11 div trigger    | :+1:       |
| tim11                | :+1:       |
| tima reload          | :+1:       |
| tima write reloading | :+1:       |
| tma write reloading  | :+1:       |

### Mooneye GB emulator-only tests

#### MBC1

| Test              | mooneye-gb |
| ----------------- | ---------- |
| bits bank1        | :+1:       |
| bits bank2        | :+1:       |
| bits mode         | :+1:       |
| bits ramg         | :+1:       |
| rom 512kb         | :+1:       |
| rom 1Mb           | :+1:       |
| rom 2Mb           | :+1:       |
| rom 4Mb           | :+1:       |
| rom 8Mb           | :+1:       |
| rom 16Mb          | :+1:       |
| ram 64kb          | :+1:       |
| ram 256kb         | :+1:       |
| multicart rom 8Mb | :+1:       |

#### MBC2

| Test              | mooneye-gb |
| ----------------- | ---------- |
| bits ramg         | :+1:       |
| bits romb         | :+1:       |
| bits unused       | :+1:       |
| rom 512kb         | :+1:       |
| rom 1Mb           | :+1:       |
| rom 2Mb           | :+1:       |
| ram               | :+1:       |

#### MBC5

| Test              | mooneye-gb |
| ----------------- | ---------- |
| rom 512kb         | :+1:       |
| rom 1Mb           | :+1:       |
| rom 2Mb           | :+1:       |
| rom 4Mb           | :+1:       |
| rom 8Mb           | :+1:       |
| rom 16Mb          | :+1:       |
| rom 32Mb          | :+1:       |
| rom 64Mb          | :+1:       |

### Mooneye GB manual tests

| Test            | mooneye-gb |
| --------------- | ---------- |
| sprite priority | :+1:       |

### Mooneye GB misc tests

| Test              | mooneye-gb |
| ---------------   | ---------- |
| boot div A        |            |
| boot div cgb0     |            |
| boot div cgbABCDE |            |
| boot hwio C       |            |
| boot regs A       |            |
| boot regs cgb     |            |

#### Bits

| Test          | mooneye-gb |
| ------------- | ---------- |
| unused hwio C |            |

#### PPU

| Test               | mooneye-gb |
| ------------------ | ---------- |
| vblank stat intr C |            |

### Test naming

Some tests are expected to pass only a single model:

* dmg = Game Boy
* mgb = Game Boy Pocket
* sgb = Super Game Boy
* sgb2 = Super Game Boy 2
* cgb = Game Boy Color
* agb = Game Boy Advance
* ags = Game Boy Advance SP

In addition to model differences, CPU revisions can affect the behaviour.
Revision 0 refers always to the initial version of a CPU (e.g. CPU CGB). AGB
and AGS use the same CPU models.  The following CPU models have several
revisions:

* DMG: 0, A, B, C
* CGB: 0, A, B, C, D, E
* AGB: 0, A, A E, B, B E. Revision E also exists, but only in Game Boy Micro
  (OXY) so it is out of this project's scope. However, A E and B E are most
  likely actually just E revision in A or B-compatible package.

In general, hardware can be divided to a couple of groups based on their
behaviour. Some tests are expected to pass on a single or multiple groups:

* G = dmg+mgb
* S = sgb+sgb2
* C = cgb+agb+ags
* A = agb+ags

For example, a test with GS in the name is expected to pass on dmg+mgb +
sgb+sgb2.

# License and copyright

Mooneye GB is licensed under GPLv3+.
Copyright (C) 2014-2020 Joonas Javanainen <joonas.javanainen@gmail.com>

The test framework and hardware tests under `tests/` are licensed
under MIT.
Copyright (C) 2014-2020 Joonas Javanainen <joonas.javanainen@gmail.com>
