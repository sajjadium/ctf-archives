

Attached is some some never-before-seen assembly code routine that we pulled off a processor which is responsible for string decryption. An input string is put into TRX register, then the routine is run, which decrypts the string.

For example, when putting UL\x03d\x1c'G\x0b'l0kmm_ string in TRX and executing this code, the resulting string in TRX is decrypted as 'tenable.ctfd.io'.

A few things we know about this assembly:

    There are only two registers, DRX and TRX. These are used to hold variables throughout the runtime.

    Operand order is similar to the AT&T syntax ,which has destination operand first and source operand 2nd ie: MOV DRX, "dogs", puts the string "dogs" into DRX register/variable. XOR TRX, DRX, xors the string held in DRX with the string in TRX and stores the result in TRX register/variable.

    There are only three instructions that this processor supports:

        XOR - XORs the destination string against a source string and stores the result in the destination string operand. The source string operand can be either literal string or string held in a register/variable. Destination operand is always register. XORs all characters against target string characters starting with beginning chars. Below is an example.

          	DRX = "dogs"
          	TRX = "shadow"
          	
          	XOR TRX, DRX

    TRX would become \x17\x07\x06\x17ow
        MOV - Simply copies the string from a source operand to the destination operand, the source string operand can be either literal or in another register as a variable.
        REVERSE - This only takes one operand, and simply reverses the string. ie: if DRX holds "hotdog" then "REVERSE DRX" turns DRX into "godtoh". The operand for this can only be a register.

What we need We need an emulator that can execute the code in the attached file in order to decrypt this string...

GED\x03hG\x15&Ka =;\x0c\x1a31o*5M

If you successfully develop an emulator for this assembly and initialize TRX with this string, execution should yield a final result in the TRX register.

