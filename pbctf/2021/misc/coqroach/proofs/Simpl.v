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

(*
 * Help! I need to complete this assignment for my advanced programming
 * languages class and I have a few things I need to prove. Maybe you can help
 * me complete this coq homework? k thx.
 *)

(* SIMPL is a Simple language with the following grammar:

e -> n | v
   | e1 + e2
   | e1 - e2
   | e1 * e2
   | e1 == e2
   | e1 != e2

s -> e | s1 ; s2 | v := e
  | if e then s1 else s2
  | while e s

In this following assignment we will define the small-step and large-step
operational semantics of the language.

*)

(* The definition of a store *)
Definition var := string.
Definition store := string -> nat.

(* 1a. Create the inductive type for expr *)
Inductive expr: Set :=
| eNum (n: nat)
| eVar (v: var)
| eAdd (e1 e2: expr)
| eSub (e1 e2: expr)
| eMul (e1 e2: expr)
| eEqu (e1 e2: expr)
| eNeq (e1 e2: expr).

(* 1b. Create the inductive type for stmt *)
Inductive stmt: Set :=
| sEmpty
| sSeq  (s1 s2: stmt)
| sStore (v: var) (e: expr)
| sCond  (cond: expr) (sTrue sFalse: stmt)
| sLoop  (cond: expr) (sBody: stmt).

(* Some notation to make your expressions/statements easier. *)
Notation "# x" := (eNum x) (at level 10, left associativity).
Notation "% x" := (eVar x) (at level 10, left associativity).
Notation "x #+ y" := (eAdd x y) (at level 40, left associativity).
Notation "x #- y" := (eSub x y) (at level 40, left associativity).
Notation "x #* y" := (eMul x y) (at level 20, left associativity).
Notation "x #== y" := (eEqu x y) (at level 50, left associativity).
Notation "x #!= y" := (eNeq x y) (at level 50, left associativity).

Notation "x #; y" := (sSeq x y) (at level 90, left associativity).
Notation "x #= y" := (sStore x y) (at level 70, right associativity).
Notation "'IIF' cond 'THEN' sTrue 'ELSE' sFalse 'ENDIF'" :=
  (sCond cond sTrue sFalse) (at level 80, right associativity).
Notation "'WHILE' cond 'DO' sBody 'DONE'" :=
  (sLoop cond sBody) (at level 80, right associativity).
Notation "'WHILE2' cond 'DO' sBody 'DONE'" :=
  (IIF cond THEN sBody #; sLoop cond sBody ELSE sEmpty ENDIF)
    (at level 80, right associativity).


(* 2. Write the update function, which takes in a variable and a number and then
 * updates the store function. *)
Definition update (st: store) (v: var) (n: nat): store :=
  fun v' => if String.eqb v v' then n else st v'.

(* 3. Define the large-step operational semantics. Remember, large-step
 * operational semanatics are judgements in the form:
 *   <e, σ> -> n
 *   <s, σ> -> σ'
 *)

(* 3a. Define largeOperExpr. *)
Reserved Notation "[ st , e ] 'EXPR' >> n" (at level 97).
Inductive largeOperExpr (st: store): expr -> nat -> Prop :=
  | LoNumb (n: nat): [st, #n] EXPR>> n
  | LoVar (v: var): [st, %v] EXPR>> (st v)
  | LoPlus (e1 e2: expr) (n1 n2: nat) (ConvE1: [st, e1] EXPR>> n1)
      (ConvE2: [st, e2] EXPR>> n2): [st, e1 #+ e2] EXPR>> n1 + n2
  | LoSub (e1 e2: expr) (n1 n2: nat) (ConvE1: [st, e1] EXPR>> n1)
      (ConvE2: [st, e2] EXPR>> n2): [st, e1 #- e2] EXPR>> n1 - n2
  | LoMul (e1 e2: expr) (n1 n2: nat) (ConvE1: [st, e1] EXPR>> n1)
      (ConvE2: [st, e2] EXPR>> n2): [st, e1 #* e2] EXPR>> n1 * n2
  | LoEquT (e1 e2: expr) (n1 n2: nat) (ConvE1: [st, e1] EXPR>> n1)
      (ConvE2: [st, e2] EXPR>> n2) (Eq: n1 = n2): [st, e1 #== e2] EXPR>> 1
  | LoEquF (e1 e2: expr) (n1 n2: nat) (ConvE1: [st, e1] EXPR>> n1)
      (ConvE2: [st, e2] EXPR>> n2) (Eq: n1 <> n2): [st, e1 #== e2] EXPR>> 0
  | LoNeqT (e1 e2: expr) (n1 n2: nat) (ConvE1: [st, e1] EXPR>> n1)
      (ConvE2: [st, e2] EXPR>> n2) (Eq: n1 <> n2): [st, e1 #!= e2] EXPR>> 1
  | LoNeqF (e1 e2: expr) (n1 n2: nat) (ConvE1: [st, e1] EXPR>> n1)
      (ConvE2: [st, e2] EXPR>> n2) (Eq: n1 = n2): [st, e1 #!= e2] EXPR>> 0
  where "[ st , e ] 'EXPR' >> n" := (largeOperExpr st e n).

(* 3b. Define largeOperStmt *)
Reserved Notation "[ st , s ] 'STMT' >> st2" (at level 97).
Inductive largeOperStmt (st: store): stmt -> store -> Prop :=
  | LoEmpty: [st, sEmpty] STMT>> st
  | LoSeq (s1 s2: stmt) (st' st'': store) (S1: [st, s1] STMT>> st')
      (S2: [st', s2] STMT>> st''): [st, s1 #; s2] STMT>> st''
  | LoStore (v: var) (e: expr) (n: nat) (ConvE: [st, e] EXPR>> n):
      [st, v #= e] STMT>> update st v n
  | LoTCond (e: expr) (n: nat) (s1 s2: stmt) (st': store)
      (Cond: ([st, e] EXPR>> n)) (NotZ: n <> 0)
      (S1: [st, s1] STMT>> st'): [st, IIF e THEN s1 ELSE s2 ENDIF] STMT>> st'
  | LoFCond (e: expr) (s1 s2: stmt) (st': store)
      (Cond: [st, e] EXPR>> 0)
      (S2: [st, s2] STMT>> st'): [st, IIF e THEN s1 ELSE s2 ENDIF] STMT>> st'
  | LoWhile (e: expr) (s': stmt) (st': store)
      (Loop: [st, WHILE2 e DO s' DONE]
          STMT>> st'): [st, WHILE e DO s' DONE] STMT>> st'
  where "[ st , s ] 'STMT' >> st2" := (largeOperStmt st s st2).

(*

4. We define a property of some SIMPL code, CONFIDENT(s, l) where s is a
statement and l is a function that returns true for all variables that need to
remain confidential. A statement s preserves the confidentiality of l, i.e.
CONFIDENT(s, l), if and only if there are no possible input stores that only
differ only by the variables in l.

 *)
Definition confidentials := var -> bool.

Definition state_conf_eq (s1 s2: store) (l: confidentials): Prop :=
(* 4a. Write a propositional function that takes in two states and a list
 * determining whether if the two states are equal, ignoring the values
 * of any confidential variables *)
  forall v, l v = true \/ (s1 v) = (s2 v).

Definition confident_stmt (s: stmt) (l: confidentials): Prop :=
(* 4b. Define a propositional function such that s preserves confidentiality of
 * variables in l *)
  forall st1 st2 st1' st2', state_conf_eq st1 st2 l -> [st1, s] STMT>> st1' ->
    [st2, s] STMT>> st2' -> state_conf_eq st1' st2' l.

Definition confident_expr (e: expr) (l: confidentials): Prop :=
(* 4c. Define a propositional function such that e preserves confidentiality of
 * variables in l *)
  forall st1 st2 n1 n2, state_conf_eq st1 st2 l -> [st1, e] EXPR>> n1 ->
    [st2, e] EXPR>> n2 -> n1 = n2.

Fixpoint usesConfidentExpr (e: expr) (l: confidentials): bool :=
(* 4d. Define a function that tests whether if e uses a confident variable *)
  match e with
  | # n => false
  | % v => l v
  | e1 #+ e2 => usesConfidentExpr e1 l || usesConfidentExpr e2 l
  | e1 #- e2 => usesConfidentExpr e1 l || usesConfidentExpr e2 l
  | e1 #* e2 => usesConfidentExpr e1 l || usesConfidentExpr e2 l
  | e1 #== e2 => usesConfidentExpr e1 l || usesConfidentExpr e2 l
  | e1 #!= e2 => usesConfidentExpr e1 l || usesConfidentExpr e2 l
  end.

Fixpoint hidesConfidentStmt (s: stmt) (l: confidentials): bool :=
(* 4e. Define a function that tests whether if s hides confident variable *)
  match s with
  | sEmpty => true
  | s1 #; s2 => hidesConfidentStmt s1 l && hidesConfidentStmt s2 l
  | v #= e => l v || negb (usesConfidentExpr e l)
  | IIF e THEN s1 ELSE s2 ENDIF =>
      negb (usesConfidentExpr e l) && hidesConfidentStmt s1 l &&
      hidesConfidentStmt s2 l
  | WHILE e DO s' DONE =>
      negb (usesConfidentExpr e l) && hidesConfidentStmt s' l
  end.

Lemma st_eq_imp_conf_eq:
  forall s1 s2 l, s1 = s2 -> state_conf_eq s1 s2 l.
Proof.
  unfold state_conf_eq. intros. rewrite H. right. reflexivity.
Qed.

Theorem hides_confidence_imp_expr:
  forall e l, usesConfidentExpr e l = false -> confident_expr e l.
Proof.
(* 4f. Complete the following proof *)
  unfold confident_expr. unfold state_conf_eq. induction e. all: simpl; intros.
  - inversion H1. inversion H2. rewrite <- H3. rewrite <- H5. reflexivity.
  - destruct (H0 v).
    + rewrite H3 in H. discriminate.
    + inversion H1. inversion H2. assumption.
  - inversion H1. inversion H2. destruct (orb_false_elim _ _ H). f_equal.
    + apply (IHe1 l H9 st1 st2). all: auto.
    + apply (IHe2 l H10 st1 st2). all: auto.
  - inversion H1. inversion H2. destruct (orb_false_elim _ _ H). f_equal.
    + apply (IHe1 l H9 st1 st2). all: auto.
    + apply (IHe2 l H10 st1 st2). all: auto.
  - inversion H1. inversion H2. destruct (orb_false_elim _ _ H). f_equal.
    + apply (IHe1 l H9 st1 st2). all: auto.
    + apply (IHe2 l H10 st1 st2). all: auto.
  - inversion H1. all: inversion H2; try reflexivity;
    destruct (orb_false_elim _ _ H).
    + assert (n0 = n4). { apply (IHe1 l H9 st1 st2). all: auto. }
      assert (n3 = n5). { apply (IHe2 l H10 st1 st2). all: auto. }
      rewrite <- H11 in Eq0. rewrite <- H12 in Eq0. destruct (Eq0 Eq).
    + assert (n0 = n4). { apply (IHe1 l H9 st1 st2). all: auto. }
      assert (n3 = n5). { apply (IHe2 l H10 st1 st2). all: auto. }
      rewrite <- H11 in Eq0. rewrite <- H12 in Eq0. destruct (Eq Eq0).
  - inversion H1. all: inversion H2; try reflexivity;
    destruct (orb_false_elim _ _ H).
    + assert (n0 = n4). { apply (IHe1 l H9 st1 st2). all: auto. }
      assert (n3 = n5). { apply (IHe2 l H10 st1 st2). all: auto. }
      rewrite <- H11 in Eq0. rewrite <- H12 in Eq0. destruct (Eq Eq0).
    + assert (n0 = n4). { apply (IHe1 l H9 st1 st2). all: auto. }
      assert (n3 = n5). { apply (IHe2 l H10 st1 st2). all: auto. }
      rewrite <- H11 in Eq0. rewrite <- H12 in Eq0. destruct (Eq0 Eq).
Qed.

Theorem stmt_induction:
  forall (P: stmt -> Prop) s,
    (P sEmpty) ->
    (forall s1 s2, P s1 -> P s2 -> P (s1 #; s2)) ->
    (forall v e, P (v #= e)) ->
    (forall cond s1 s2, P s1 -> P s2 -> P (IIF cond THEN s1 ELSE s2 ENDIF)) ->
    (forall cond s', P s' -> P (WHILE2 cond DO s' DONE) ->
      P (WHILE cond DO s' DONE)) ->
    P s.
  intros P s PEmpty PSeq PAssign PIf PWhile.
  induction s. all: try auto.
  (*
  assert (not (P (WHILE cond DO s DONE)) -> not (P (WHILE2 cond DO s DONE))).
  { specialize (PWhile cond s IHs). unfold not. intros. auto. }
  assert (not (P (WHILE cond DO s DONE)) -> False).
  { intros PNoWhile. apply PNoWhile. apply PWhile. apply IHs. apply PWhile2.
  }
  assert (not (P (WHILE cond DO s DONE)) -> not (P (WHILE2 cond DO s DONE))).
  { specialize (PWhile cond s IHs). unfold not. intros. auto. }
  destruct (PExclude_middle (WHILE cond DO s DONE)).
  - assumption.
  - apply H in H0. unfold not in H0. apply PWhile. apply IHs. apply PIf.
  unfold not in H.
*)
Admitted.

Definition P_hides_confidence_imp_stmt (s: stmt) :=
  forall l, hidesConfidentStmt s l = true -> confident_stmt s l.

Theorem hides_confidence_imp_stmt:
  forall s, P_hides_confidence_imp_stmt s.
Proof.
  intro. apply stmt_induction.
(* 4g. Complete the following proof *)
  all: unfold P_hides_confidence_imp_stmt.
  - unfold confident_stmt. unfold state_conf_eq. intros. inversion H1. inversion H2.
    rewrite <- H4. rewrite <- H5. apply H0.
  - unfold confident_stmt. unfold state_conf_eq. simpl.
    intros s1 s2 IHs1 IHs2 l H st1 st2 st1' st2' H1 H2 H3 v.
    destruct (andb_prop _ _ H).
    inversion H2. inversion H3. apply (IHs2 _ H4 st' st'0).
    apply (IHs1 _ H0 st1 st2). all: assumption.
  - unfold confident_stmt. simpl. intros. inversion H1. inversion H2.
    unfold state_conf_eq. intros. destruct (l v) eqn: Cv.
    + unfold update. destruct (v =? v2)%string eqn:Evv2.
      -- left. apply String.eqb_eq in Evv2. rewrite <- Evv2. assumption.
      -- destruct (H0 v2). all: auto.
    + destruct (l v2) eqn: Cv2. left. reflexivity.
      right. destruct (orb_prop _ _ H). discriminate.
      apply negb_true_iff in H9. apply hides_confidence_imp_expr in H9.
      unfold update. destruct (v =? v2)%string eqn:Evv2.
      -- unfold confident_expr in H9. apply (H9 st1 st2). all: auto.
      -- destruct (H0 v2). rewrite H10 in Cv2. discriminate. assumption.
  - unfold confident_stmt. simpl. intros cond s1 s2 IHs1 IHs2. intros.
    apply andb_prop in H. destruct H. apply andb_prop in H. destruct H.
    apply negb_true_iff in H. apply hides_confidence_imp_expr in H.
    unfold confident_expr in H. inversion H1.
    + inversion H2.
      -- apply (IHs1 l H4 st1 st2 st1' st2'). all: assumption.
      -- exfalso. apply NotZ. apply (H st1 st2 n 0 H0 Cond Cond0).
    + inversion H2.
      -- exfalso. apply NotZ. symmetry. apply (H st1 st2 0 n H0 Cond Cond0).
      -- apply (IHs2 l H3 st1 st2 st1' st2'). all: assumption.
  - simpl. intros cond s' Hinner Hwhile2 l H. unfold confident_stmt.
    intros. inversion H1. inversion H2. unfold confident_stmt in Hwhile2.
    assert (negb (usesConfidentExpr cond l) && (hidesConfidentStmt s' l &&
           (negb (usesConfidentExpr cond l) && hidesConfidentStmt s' l)) &&
           true = true) as Hpre.
    { rewrite H. destruct (andb_prop _ _ H). rewrite H9. rewrite H10.
      reflexivity. }
    apply (Hwhile2 l Hpre st1 st2 st1' st2' H0 Loop Loop0).
Qed.

Theorem confidence_hides_imp_expr:
  forall e l, confident_expr e l -> usesConfidentExpr e l = false.
Proof.
(* 4h. Now prove the converse *)
Abort.

Definition P_confidence_hides_imp_stmt (s: stmt) :=
  forall l, confident_stmt s l -> hidesConfidentStmt s l = true.

Theorem confidence_hides_imp_stmt:
  forall s, P_confidence_hides_imp_stmt s.
Proof.
(* 4i. Complete this proof *)
Abort.
