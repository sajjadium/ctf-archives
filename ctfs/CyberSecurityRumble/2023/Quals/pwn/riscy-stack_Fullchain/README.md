Enter a realm where hackers dare,
Chaining exploits, a challenge rare.
First, a userspace binary to deceive,
Then a custom kernel, secrets to retrieve.
Lastly, a patched firmware stands tall,
Break its defenses, conquer them all.
So, embrace the challenge, the exploits untold,
Discover the beauty, where minds are bold.
This is the final challenge of riscy-stack: Combine the three exploits for the individual stages into a full chain.


# riscy-stack: Fullchain

`riscy-stack` consists of a simple userspace application, running on top of a custom kernel, running
on top of patched firmware, all in RISC-V. Each of the three stages is first solved independently of
the other stages for one flag each, then you can chain your exploits to get a bonus flag.

Combine the three exploits for the individual stages into a full chain. The location of the flag in
the firmware image is marked with `CSR{fw_ZZZZZZZZZZZZZZZZ}`, I used a hex editor to insert the flag
on the remote, so otherwise it has the exact same binary. The flag is different from the one for the
firmware stage of course, it actually starts with `full_`.

Here's the full poem as a treat:

```
In a realm of challenges, intriguing and grand,
Where mind and wit together take a stand,
A quest awaits the daring and the bold,
A chain of exploits, a tale yet untold.

Three stages unfold, each with its own might,
A journey through layers, concealed in the night.
With subtle steps, in code's mysterious dance,
Players shall endeavor, seizing every chance.

First, a userspace binary shall you deceive,
With crafty exploits, its defenses you'll cleave.
The silent conqueror, with audacity entwined,
Shall break the barriers, freedom aligned.
In this realm, where code dances in light,
Unleash your skills, exploit with all your might.

Unveiling the flaws, the vulnerability's trace,
A door opens wide to a kernel's embrace.
The second realm, where custom powers reside,
A realm of dreams, where security hides.
Through clever tricks and cunning arrays,
A gateway appears, in the kernel's maze.

But beware, for beyond this digital plane,
A patched firmware guards secrets arcane.
For here, in the heart of the machine,
Lies the gate to power, yet unseen.
The final stage, presumed invincible,
Yet a spark of hope, unseen and indivisible.

Chained exploits, a symphony of art,
Where each step taken, ignites the spark.
The exploit unfolds, like petals of a rose,
Revealing the strength that quietly grows.
With binary, kernel, and firmware held tight,
Forge connections, where differences ignite.

So gather your tools, your wits honed with care,
Embark on this journey, the challenge to dare.
For in this quest, where only the skilled prevail,
The victor shall stand, their prowess we hail.
```
