# Language Spec v2 for ICICLE (Imaginary Ctf Instruction Collection for Learning assEmbly)

## Writing Code in ICICLE

Each line contains an instruction, label, or comment. Instructions should be formatted like the following:

`add r1, r2, 5`

That is, there should be a single space after the command name, and then arguments should be separated by a comma and a space. Arguments can be a int, string, register, **or dereferenced memory location**.

**A label is a string, followed by a ":", like the following:
```
main:
```
This does not have any effect when run, but instead labels a section of code to be jumped to later.**

Comments are any line that begin with a `#`, and these are skipped. Additionally, you can place a comment after an instruction, to similarly no effect.

Whitespace at the beginning/end of lines is ignored.

### Registers

There are 17 registers, all of which are initialized to 0. There are 16 general purpose registers, named `r0` through `r15`. These can take **infinite-precision** ints or string values. **There is also the `rip`, or instruction pointer, register. This register points to the next instruction to be executed at all times. It can only take int values, but can be read or set just like a normal register.**

### Memory and Dereferencing (new!)

The language has 2\*\*16 memory locations, addressed from 0 to 2\*\*16-1. Each of these, like registers, can take an int or string value. A memory location can be dereferenced with square brackets (`[]`). `[5]` denotes the memory value at address 5, and `[r1]` denotes the memory value at the location in `r1`. You can dereference multiple times, so `[[5]]` denotes the memory value at the memory value at address 5.

## Instructions

A complete list of instructions can be found below:
```
Arithmetic:
add
sub
mult
div
mod
xor
and
or
rev
mov

Type Conversion:
strint
intstr

I/O:
pr
readstr
readint

Control Flow (new!):
j
jnz
jz
jl
```

### Arithmetic Instructions
All instructions in this section take 2 or 3 arguments, denoted here as `a0, a1, a2`. For all instructions, an operation is performed on `a1` and `a2`, and the result stored in `a0`.

#### add
If both a1 and a2 are ints, adds them and stores the result in a0. Otherwise, converts both to strings and adds (e.g. `add r1, "test", 0` will store "test0" in r1).
#### sub
Calculates `a1-a2` and stores the result in a0. Only valid for ints.
#### mult
Only valid if at least one of a1, a2 is an int. If both are ints, stores `a1*a2` in `a0`. If a1 is a string, repeats a1 a2 times, and stores the result in a0, and same goes for if a2 is a string (e.g. `mult r1, 'a', 5` and `mult r1, 5, 'a'` both store "aaaaa" in r1).
#### div
Calculates `a1//a2` (where `//` denotes integer division) and stores the result in a0. Only valid for ints.
#### mod
Calculates `a1%a2` (where `%` denotes modulo) and stores the result in a0. Only valid for ints.
#### xor
If both a1 and a2 are ints, calculates the bitwise xor and stores the result in a0. If at least one is a string, convert any ints to strings as by `intstr`, then compute the xor of the two strings as follows:
- The result will be the length of the longer string
- For each character in the longer string, bitwise xor the character code with the character at the same index (mod the shorter string length) in the shorter string

#### and
Calculates the bitwise and of a1 and a2, and stores the result in a0. Only valid for ints.
#### or
Calculates the bitwise or of a1 and a2, and stores the result in a0. Only valid for ints.
#### rev
Only takes 2 args. If a1 is a string, reverses it and stores the result in a0 ("abc" -> "cba"). If a1 is an int, converts it to a string, reverses it, converts back to an int, and stores the result in a0 (123 -> 321).
#### mov
Only takes 2 args. Moves a1 to a0.

### Type Conversion Instructions
Both of these take two args - converting a1 and storing the result in a0.
#### strint
Converts a string in a1 into an int, and stores it in a0. It does so by converting each **byte** in the string to hexadecimal, concatenating all of the characters into a large hexadecimal number, and converting that to base 10.
#### intstr
Converts an int in a1 into a string, and stores it in a0. The int cannot be negative. This is the opposite process of `strint` - the number is converted into hex, then every 2 hex digits are converted into a **byte. This bytestring is encoded into a string with extended ascii encoding - essentially, every byte is treated as its own character.**

### I/O Instructions
These each take one argument.
#### pr
Prints a0. If a0 is a string, prints the string. If a0 is an int, prints the int.
#### readstr
Reads a string from stdin to a0.
#### readint
Reads an int from stdin to a0.

### Control Flow Instructions
#### j
Takes one argument, the name of a label. Immediately jumps to the label. For example, the following code will loop infinitely.
```
main:

j main
```
#### jnz
Takes two args, a value and the name of a label. If a0 is not zero, jump to the label. For example, the following code will loop 10 times.
```
mov r1, 10
loop:
sub r1, r1, 1
jnz loop
```
#### jz
Takes two args, a value and the name of a label. If a0 is zero, jump to the label. For example, the following code will loop 10 times.
```
mov r1, 10
loop:
sub r1, r1, 1
jz end
j loop

end:
```
#### jl
Takes three args, two values and the name of a label. If a0 is less than a1, jump to the label. For example, the following code will loop 10 times.
```
mov r1, 0
loop:
add r1, r1, 1
jl r1, 10, loop
```
