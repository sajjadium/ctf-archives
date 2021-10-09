From CTF Require Import Simpl.

Require Import Arith.
Require Import Bool.
Require Import List.
Require Import Nat.
Require Import Coq.Strings.String.
Require Import Coq.Program.Equality.

Open Scope bool_scope.
Open Scope list_scope.
Open Scope string_scope.
Open Scope nat_scope.

(* This will be overriden by the challenge, and is just a sample file of what
 * it will look like. You can use this as a testing grounds, just pop this file
 * into coqide, and you should be able to immediately use it and interactively
 * play with the proofs. *)

(* Here are the tutorial problems *)
Theorem conj1: forall P Q: Prop,
  P /\ Q -> Q.
Proof.
Admitted.

Theorem transitive: forall P Q R: Prop,
  (P -> Q) -> (Q -> R) -> P -> R.
Proof.
Admitted.

Theorem or_logic: forall A B C D: Prop,
  (A -> B) -> (C -> D) -> A \/ C -> B \/ D.
Proof.
Admitted.

Theorem not_true_is_false: forall b: bool,
  b <> true -> b = false.
Proof.
Admitted.

Theorem mult_plus_distr_r : forall n m p : nat,
  (n + m) * p = (n * p) + (m * p).
Proof.
Admitted.

Theorem conv_ex1:
  [update (update (fun _ => 0) "a" 2) "b" 3,
   #23 #+ %"a" #* %"b" #- (#1 #== #0)] EXPR>> 29.
Proof.
Admitted.

Theorem conv_ex2: forall st,
  [fun _ => 0,
    "a" #= #1 #+ #2 #;
    "b" #= %"a" #+ #1] STMT>> st -> st "b" = 4.
Proof.
Admitted.

Theorem conv_ex3: forall st,
  [fun _ => 0,
    "a" #= #2 #;
    "b" #= #2 #;
    "x" #= #0 #;
    WHILE %"b" #!= #0 DO
      "x" #= %"x" #+ %"a" #;
      "b" #= %"b" #- #1
    DONE] STMT>> st -> st "x" = 4.
Proof.
Admitted.


(* For flag 1 *)
Theorem confidence_hides_imp_stmt:
  forall s, P_confidence_hides_imp_stmt s.
Proof.
Admitted.

(* For flag 2 *)
Theorem confidence_hides_imp_expr:
  forall e l, confident_expr e l -> usesConfidentExpr e l = false.
Proof.
Admitted.

