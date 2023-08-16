import textwrap

import ed25519
from hexdump import hexdump

from mcu import MCU

DEMO_PROGRAM = textwrap.dedent(
    r"""
    with get_logfile(now().isoformat()) as logfile:
        logfile.write("Program started.\n")
        for i in range(13):
            print(chr(mcu.read(mcu.DYNAMIC_DATA_SEGMENT_OFFSET + i)), end="")
        print()
        logfile.write("Program finished.\n")
    """
)


def flash_demo_image(mcu):
    signing_key, verifying_key = ed25519.create_keypair()

    program = DEMO_PROGRAM.encode()
    signature = signing_key.sign(program)

    mcu.flash(MCU.STATIC_DATA_SEGMENT, verifying_key.to_bytes())
    mcu.flash(MCU.DYNAMIC_DATA_SEGMENT, "Hello, world!".encode())
    mcu.flash(MCU.PROGRAM_INSTRUCTION_SEGMENT, program, signature)


def main():
    mcu: MCU = None

    while True:
        print(
            textwrap.dedent(
                """
                Main menu:
                1. Create new MCU.
                2. Flash segment.
                3. Dump segment.
                4. Run MCU.
                5. Exit.
                """
            )
        )

        choice = input("Choice: ")

        if choice == "1":
            mcu = MCU()
            flash_demo_image(mcu)

        elif choice == "2":
            if mcu is None:
                raise Exception("No MCU found.")

            segment = int(input("Segment: "))
            image = bytes.fromhex(input("Image: "))
            signature = bytes.fromhex(input("Signature: "))
            mcu.flash(segment, image, signature)

        elif choice == "3":
            if mcu is None:
                raise Exception("No MCU found.")

            segment = int(input("Segment: "))
            print("Content: ")
            hexdump(mcu.dump(segment))

        elif choice == "4":
            if mcu is None:
                raise Exception("No MCU found.")

            try:
                mcu.run()
            except Exception as e:
                print("The MCU crashed with error:", e)
                break

        elif choice == "5":
            break


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occured: {e}")
