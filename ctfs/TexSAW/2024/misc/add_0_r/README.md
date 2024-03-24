These proof questions aim to introduce you to the Coq Proof System, an ecosystem of tools used to formally verify mathematical propositions, and specifically the correctness of programs.

Write a formal proof in the Coq system stating that for all natural numbers n, n + 0 = n.

In Coq, this is stated as:

Theorem add_0_r :
    forall n, n + 0 = n.

You will submit the text of your proof as a payload to 3.23.56.243 9014 where it will be checked for correctness. If your proof does indeed prove add_0_r, you will be provided the flag. Make sure to start with Proof. and end with Qed. followed by EOF on its own line.

Format: texsaw{flag}
