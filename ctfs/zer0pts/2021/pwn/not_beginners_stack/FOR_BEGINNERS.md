# Not Beginner's Stack
Beginner's Guidebook

## 1. Introduction to Stack
Do you understand what a stack frame is?
Let's trace the following code and see what happens on the stack.
```
call function  ; [1]
mov edx, eax
...

function:
push rbp       ; [2]
mov rbp, rsp   ; [3]
sub rsp, 0x10  ; [3]
lea rdi, [rbp-0x10]
call gets
leave          ; [4]
ret            ; [5]
```
First, the code calls `function` at [1].
Before calling the function, the initial stack looks like (a) in the figure below.

After `call` instruction runs, the return address is pushed onto the stack top like (b).
The return address is the address of the next instruction after the caller.
This time, the address of `mov edx, eax` instruction is pushed onto the stack.
```
|          |       |          |       |          |       |          |
+----------+       +----------+       +----------+       +rsp-------+
|          |       |          |       |          |       |  local   |
|          |       |          |       |          |       | variables|
+----------+       +----------+       +rsp-------+       +rbp-------+
|          |       |          |       | saved bp |       | saved bp |
+----------+  [1]  +rsp-------+  [2]  +----------+  [3]  +----------+
|   ....   | ----> | ret addr | ----> | ret addr | ----> | ret addr |
+rsp-------+       +----------+       +----------+       +----------+
|   ....   |       |   ....   |       |   ....   |       |   ....   |
    (a)                (b)                (c)                (d)
```
Now we're in the callee function.
The function creates a stack frame at [2] and [3].
First, it saves the base pointer (RBP) at [2] like (c) in the figure.
RBP is used for referencing the local variables.
As we're entering a different scope, we need to save the base pointer.

Then, the new base pointer is set to the stack top (RSP) at [3].
When the function uses a/some local variable(s), the total size of the variables are subtracted from RSP like (d).
This sequence of operations can be done by `enter` instruction as well.
However, this instruction is rarely used due to performance issues.

The function can now use the local variable by referencing [rbp-0x??].
Next, let's see what happens when leaving the function.
```
|          |       |          |       |          |
+rsp-------+       +----------+       +----------+
|  local   |       |          |       |          |
| variables|       |          |       |          |
+rbp-------+       +----------+       +----------+
| saved bp |       |          |       |          |
+----------+  [4]  +rsp-------+  [5]  +----------+
| ret addr | ----> | ret addr | ----> |          |
+----------+       +----------+       +rsp-------+
|   ....   |       |   ....   |       |   ....   |
    (d)                (e)                (f)
```
`leave` instruction works as `mov rsp, rbp; pop rbp;`.
This instruction restores the state like (e) in the figure above.
Finally, `ret` instruction pops the value at the stack top and sets instruction pointer (RIP) to the return address.
This way, we can call any functions from anywhere and return to correct places.

## 2. Introduction to Stack Buffer Overflow
If buffer overflow happens, the saved base pointer and the return address will be overwritten like the figure below.
```
|          |            |          |
+rsp-------+            +rsp-------+
|  local   |            | AAAAAAAA |
| variables|            | AAAAAAAA |
+rbp-------+            +rbp-------+
| saved bp |   buffer   | AAAAAAAA |
+----------+  overflow  +----------+
| ret addr | ---------> | BBBBBBBB |
+----------+            +----------+
|   ....   |            |   ....   |
```
In this case, RBP becomes "AAAAAAAA" and `ret` instruction tries to jump to "BBBBBBBB".
Pwners abuse this vulnerability to control RIP to wherever they want to jump.

## 3. Design of This Challenge
In this challenge, the program defines own `call`/`ret` instructions.
```
%macro call 1
;; __stack_shadow[__stack_depth++] = return_address;
  mov ecx, [__stack_depth]
  mov qword [__stack_shadow + rcx * 8], %%return_address
  inc dword [__stack_depth]
;; goto function
  jmp %1
  %%return_address:
%endmacro

%macro ret 0
;; goto __stack_shadow[--__stack_depth];
  dec dword [__stack_depth]
  mov ecx, [__stack_depth]
  jmp qword [__stack_shadow + rcx * 8]
%endmacro
```
It doesn't save the return address on the stack but saves it into an array at the bss section.
Since we don't have the return address on the stack, the attacker can't abuse stack overflow to overwrite the return address :)

## 4. Hint
So, you can't simply overwrite the return address.
As mentioned in Chapter 2, the attacker can overwrite not only the return address but also the saved base pointer.
What can an attacker do by overwriting the base pointer?

Also, don't forget to check the security mechanism of the program (i.e. SSP, DEP and PIE).

----

Apology for my poor English :P
Hope you now understand how the stack frame is created, as well as how `call` and `ret` works!
