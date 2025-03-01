
## **"Chrono Specter: The Phantom Execution"**

---

The CPU operates in a peculiar manner:

- It follows a strict **instruction set**, allowing data to be **loaded, stored, printed, and flushed**
```custom
# Load value from memory into a register
load $rX address       # rX ← MEM[address]
load $rX offset($rY)   # rX ← MEM[rY + offset]

# Store register value into memory
set $rX address        # MEM[address] ← rX

# Print register value
print $rX             # Output value of rX

# Flush memory address from cache
flush address         # Removes address from cache

```
- It lacks traditional **branching**, moving forward like an unstoppable specter through each batch of commands.
```custom
batch:
load $r1 10
print $r1

batch:
load $r2 4($r1)
set $r2 20
print $r2

```

**Output**
```
output of first batch

output of second batch

```

```
error code 1//out of bound exception
error code 2//unknown register
error code 3//unknown command
```
- And most curiously, it **executes speculatively**, racing ahead before verifying permissions—rewinding only if reality proves it wrong.

But this flaw, this _temporal drift_, hints at something more. If one were to carefully manipulate the execution flow, to trick the **Chrono Engine** into glimpsing forbidden memory before it realizes its mistake… perhaps the past could be rewritten.
