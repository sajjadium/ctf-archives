unvariant

https://lkml.org/lkml/2012/2/10/356. The zig version used is 0.13.0. A small patch was applied to ArrayListAlignedUnmanaged.ensureTotalCapacity to mark the function as noinline to prevent miscompilation issues.

