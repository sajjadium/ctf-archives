
The system you are exploiting is running a custom Mongoose V RAD hardened MIPS processor, by Synova Inc. The provided emulator runs the firmware and if you pay attention with it starts up, will show where hardware devices are mapped into the physical address space.  Start the emulator with the following command line:

./vmips -o fpu -o memsize=3000000 firmware.rom

