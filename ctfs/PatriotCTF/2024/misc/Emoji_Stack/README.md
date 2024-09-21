Welcome to Emoji Stack, the brand new stack based emoji language! Instead of other stack based turing machines that use difficult to read and challenging characters like + - and [], Emoji Stack uses our proprietary patent pending emoji system.

The details of our implentation is below:

    👉: Move the stack pointer one cell to the right
    👈: Move the stack pointer one cell to the lef
    👍: Increment the current cell by one, bounded by 255
    👎: Decrement the current cell by one, bounded by 0
    💬: Print the ASCII value of the current cell
    🔁##: Repeat the previous instruction 0x## times

The Emoji Stack is 256 cells long, with each cell supporting a value between 0 - 255.

As an example, the program "👍🔁47💬👉👍🔁68💬👉👍🔁20💬" Would output "Hi!" with the following execution flow:

[0, 0, 0, 0] 👍🔁47

[0x48, 0, 0, 0] 💬👉: H

[0x48, 0, 0, 0] 👍🔁68

[0x48, 0x69, 0, 0] 💬👉: i

[0x48, 0x69, 0, 0] 👍🔁20

[0x48, 0x69, 0x21, 0] 💬: !

Author: CACI
