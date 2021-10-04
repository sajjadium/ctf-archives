 I love breaking analyses proven to be safe.

nc 35.221.114.187 30001
Hint 1.

I heard "value restriction" is important for the soundness of
the OCaml type system.
Hint 2.

Well, you may think this chall is "unsound hole challenge of
the strange (non-famous?) language"?

This is "partially" no.
First, OCaml is famous! :)

Joking aside (not joking!),
you may notice that this challenge

    complies to an OCaml VM binary (not native binary!) using ocamlc (not ocamlopt)
    executes the VM binary using ocamlrun

Here pro tips: OCaml's VM interpreter is implemented in C!
(c.f. https://github.com/ocaml/ocaml/tree/4.12/runtime)

That means ...
Let's just leave it at that.
