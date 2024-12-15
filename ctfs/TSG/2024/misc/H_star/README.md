Author: moratorium08

This paper introduces a refinement type system for Haskell. We have developed a prototype tool, referred to as H*. The tool processes Haskell programs annotated with refinement types, transforming them into equivalent F* programs. Using F*'s proof engine, the safety of the program is verified. Upon successful verification, the refinement type annotations are removed, and the original program is compiled with GHC for execution.

Our empirical evaluation demonstrates the effectiveness of this tool across various real-world programs. This efficacy is primarily attributable to the robust proof engine provided by F*.
