This is an encoding of a non-empty list - that is, a list that has at least one element:

Inductive nonempty_list (X : Type) : Type :=
    | single : X -> nonempty_list X
    | ncons : X -> nonempty_list X -> nonempty_list X.
Arguments nonempty_list X : assert.
Arguments single {X}.
Arguments ncons {X}.

Notation "[ x ]" := (single x).
Notation "x :: y" := (ncons x y).
Notation "[ x ; .. ; y ; z ]" := (ncons x (.. (ncons y (single z)) ..)).

This is a recursive function that interleaves two non-empty lists. That is, interleave [1;3;5;7;9] [2;4;6;8;10] = [1;2;3;4;5;6;7;8;9;10]. If the lists do not have matching lengths, the matching sections are interleaved, and the remainder of the longer list is appended to the result.

Fixpoint interleave {X : Type} (a b : nonempty_list X) : nonempty_list X :=
    match a, b with
    | [ha], [hb] => [ha; hb]
    | [ha], hb :: tb => ha :: hb :: tb
    | ha :: ta, [hb] => ha :: hb :: ta
    | ha :: ta, hb :: tb => ha :: (hb :: (interleave ta tb))
    end.

This is an inductive proposition that characterizes a nonempty list such that each of its elements is less than or equal to the next element. For example, nl_le [1;3;100;9999] is provable, but nl_le [1;2;3;4;5;4] is not provable.

Inductive nl_le : nonempty_list nat -> Prop :=
| le_single : forall x, nl_le (single x)
| le_two : forall x y, x <= y -> nl_le (x :: [y])
| le_pair : forall a b tl,
    a <= b -> nl_le (b :: tl) -> nl_le (a :: b :: tl).

Write a formal proof in the Coq system stating that for two non-empty lists a and b, if nl_le (interleave a b) is True, then both nl_le a and nl_le b are True.

Theorem le_interleave :
    forall (a b : nonempty_list nat),
    nl_le (interleave a b) ->
    nl_le a /\ nl_le b.

This is a big proof, so I've provided some very useful helper lemmas for you, and I've written most of the proof as well. Download them here. Make sure to use these resources! You will submit the text of your proof as a payload to 3.23.56.243 9015 where it will be checked for correctness. If your proof does indeed prove le_interleave, you will be provided the flag. Be sure to submit everything between the last Proof. and Qed., inclusive, followed by EOF on its own line.

Format: texsaw{flag}
