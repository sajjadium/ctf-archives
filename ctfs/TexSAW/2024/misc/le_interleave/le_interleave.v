Inductive nonempty_list (X : Type) : Type :=
    | single : X -> nonempty_list X
    | ncons : X -> nonempty_list X -> nonempty_list X.
Arguments nonempty_list X : assert.
Arguments single {X}.
Arguments ncons {X}.

Notation "[ x ]" := (single x).
Notation "x :: y" := (ncons x y).
Notation "[ x ; .. ; y ; z ]" := (ncons x (.. (ncons y (single z)) ..)).

Fixpoint interleave {X : Type} (a b : nonempty_list X) : nonempty_list X :=
    match a, b with
    | [ha], [hb] => [ha; hb]
    | [ha], hb :: tb => ha :: hb :: tb
    | ha :: ta, [hb] => ha :: hb :: ta
    | ha :: ta, hb :: tb => ha :: (hb :: (interleave ta tb))
    end.

Definition hd {X : Type} (l : nonempty_list X) := match l with [x] => x | x :: y => x end.

Inductive nl_le : nonempty_list nat -> Prop :=
| le_single : forall x, nl_le (single x)
| le_two : forall x y, x <= y -> nl_le (x :: [y])
| le_pair : forall a b tl, 
    a <= b -> nl_le (b :: tl) -> nl_le (a :: b :: tl).

#[local] Hint Constructors nl_le : core.

Require Import Nat.
Require Import PeanoNat.

Lemma le_other : 
    forall x n tl,
    x <= n -> nl_le (n :: tl) -> nl_le (x :: tl).
Proof.
    induction tl; intros.
    - inversion H0; subst. apply le_two. 
        now apply (Nat.le_trans _ n).
    - inversion H0; subst.
        apply le_pair. now apply (Nat.le_trans x n x0).
        assumption.
Qed.

Lemma le_hd : 
    forall x tl,
    nl_le tl ->
    x <= hd tl ->
    nl_le (x :: tl).
Proof.
    induction tl; intros.
    - simpl in H0. now apply le_two.
    - now apply le_pair.
Qed.

Lemma nl_le_sublist : 
    forall hd tl,
    nl_le (hd :: tl) -> 
    nl_le tl.
Proof.
    induction tl; intros.
    - constructor.
    - now inversion H; subst.
Qed. 

Lemma hd_interleave :
    forall {X : Type} (a b : nonempty_list X),
    hd (interleave a b) = hd a.
Proof.
    intros. destruct a, b; reflexivity.
Qed.

(* This is the proof to solve *)
Theorem le_interleave : 
    forall (a b : nonempty_list nat),
    nl_le (interleave a b) ->
    nl_le a /\ nl_le b.
Proof.
    induction a; intros.
    - destruct b.
        -- (* SOLVE HERE *) admit.
        -- (* SOLVE HERE *) admit.
    - destruct b; simpl in *.
        -- inversion H; subst. 
            (* SOLVE HERE *) admit.
        -- split; (apply le_hd; 
            [now apply (IHa b), (nl_le_sublist n), (nl_le_sublist x)|idtac]).
            ++ rewrite <- (hd_interleave a b).
                inversion H; inversion H4; subst; simpl in *.
                (* SOLVE HERE *) admit.
                (* SOLVE HERE *) admit.
            ++ apply (Nat.le_trans _ (hd a)).
                inversion H; inversion H4; subst; simpl in *.
                now rewrite <- (hd_interleave a b), <- H7.
                assert (b1 = hd (interleave a b)). {
                    rewrite <- H6. reflexivity.
                } subst. now rewrite hd_interleave in H7.
                repeat apply nl_le_sublist in H.
                inversion H; destruct a, b.
                    1-4: inversion H1.
                    all: inversion H0; subst;
                        assumption.
Qed.
