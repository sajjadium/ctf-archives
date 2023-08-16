import threading
from avatar2 import *
from avatar2.peripherals.avatar_peripheral import AvatarPeripheral
import signal
import sys
import time

firmware = abspath("/firmware.bin")


class IOPeripheral(AvatarPeripheral):
    def hw_read(self, offset, size):
        if offset == 4:
            if self.char != None:
                return 1
            self.char = sys.stdin.buffer.read(1)
            return 0
        ret = int.from_bytes(self.char, byteorder="little")
        self.char = None
        return ret

    def hw_write(self, offset, size, value: int):
        sys.stdout.buffer.write(value.to_bytes(size, byteorder="little"))
        sys.stdout.flush()
        return True

    def __init__(self, name, address, size, **kwargs):
        AvatarPeripheral.__init__(self, name, address, size)
        self.char = None
        self.read_handler[0:size] = self.hw_read
        self.write_handler[0:size] = self.hw_write


def main():
    avatar = Avatar(arch=ARM_CORTEX_M3, output_directory="/tmp/avatar")

    avatar.add_memory_range(
        0x00000000, 128 * 1024, file=firmware, name="flash", permissions="rwx"
    )

    avatar.add_memory_range(0x20000, 64 * 1024, name="ram", permissions="rw-")

    hw = avatar.add_memory_range(
        0x40004C00, 0x100, name="io", emulate=IOPeripheral, permissions="rw-"
    )

    qemu = avatar.add_target(
        QemuTarget, cpu_model="cortex-m3", entry_address=1  # force thumb
    )
    avatar.init_targets()
    qemu.write_register("sp", qemu.read_memory(0x0, 4, 1))
    qemu.write_register("pc", qemu.read_memory(0x4, 4, 1))

    def signal_handler(signal, frame):
        avatar.stop()
        avatar.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    avatar.load_plugin("gdbserver")

    avatar.spawn_gdb_server(qemu, 1234, True)
    qemu.cont()

    qemu.wait(TargetStates.EXITED)


if __name__ == "__main__":
    main()
