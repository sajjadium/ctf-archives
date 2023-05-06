# Fun type system

## How to run
Run `sbt`, then, in the `sbt:fun-type-system>` prompt, run `compile`. While you keep the sbt prompt open, sbt will use partial recompilation on subsequent `compile`s, which substantially speeds it up.
Be patient, a successful clean build takes 5m on my laptop to compile ;)

## What to do
Change the `type Flag = ...` line to enter the flag. If the program compiles, congrats! you won. Please keep the ` =~:` after the last character.
The string entered as Flag does not contain `EPFL{...}`, it is only the string inside the curly brackets (if Flag was ABCD then the flag would be`EPFL{ABCD}`).
