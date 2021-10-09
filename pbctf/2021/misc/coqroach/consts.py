disallowed = '''
admit
Admitted
Axiom
Axioms
Conjecture
Conjectures
Extraction
Parameter
Parameters
Hypothesis
Hypotheses
Variable
Variables
Canonical
Redirect
Require
Import
Export
Load
Print
Add
LoadPath
Cd
Pwd
Remove
Quit
Drop
Timeout
Fail
Declare
Reduction
Checking
Unset
bypass_check
Register
Primitive
Warnings
Search
'''.lower().strip().split('\n')

chall_header = '''
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

'''

check_header = '''
From CTF Require Simpl.
From CTF Require SimplChall.

'''

intro_prompt = '''
I need help on a homework assignment, please help me!  If you see the attached
handout, I wrote some proofs, stuck on the last two proofs. Maybe you can help
me?

Oh wait, you haven't used this before? Let's go through some tutorial
challenges. Do you want to do them or skip them?'''

tut_intro = '''
Coq has a lot of automated tactics. We encourage you to refrain from using
them for now, since you can very easily use those to solve these earlier
challenges, but for some later challenges you will not be able to do the same :P

Lets start with some basic logic:
'''

tut_induct = '''
Nice, nice. Now let's try a more complex proof. This one you'll have to write
your own theorem header:

Theorem mult_plus_distr_r : forall n m p : nat,
  (n + m) * p = (n * p) + (m * p).

Copy the above without modifying anything. You may find that you will have to
prove some lemmas about it.
'''

induct_check = check_header + '''
Check SimplChall.mult_plus_distr_r : forall n m p : nat,
  (n + m) * p = (n * p) + (m * p).
'''

tut_ind_prop = '''
Great! Now lets get to my homework. I used inductive propositions to specify the
large-step operational semantics of this language. Feel free to check out the
associated file for more details.

(Hint: Look at https://softwarefoundations.cis.upenn.edu/lf-current/IndProp.html
before attempting these challenges).

Let's start by proving some code "converges" to some value/state. The first one
involves an inductive proposition in the conclusion so you would apply the
constructors or "rules" of the inductive property:

Theorem conv_ex1:
  [update (update (fun _ => 0) "a" 2) "b" 3,
   #23 #+ %"a" #* %"b" #- (#1 #== #0)] EXPR>> 29.
'''

tut_ind_prop2 = '''
Okay, let's try this one. When the inductive proposition is in the
premise/hypothesis, we should destruct the rule. You should use the special
"inversion" tactic on it:

Theorem conv_ex2: forall st,
  [fun _ => 0,
    "a" #= #1 #+ #2 #;
    "b" #= %"a" #+ #1] STMT>> st -> st "b" = 4.

'''

tut_ind_prop3 = '''
Wow that was kinda tedious. So to make it nicer, we wrote a few tactics that
might help you:

Ltac next_with H := inversion H; subst; clear H; simpl in *.

Ltac unseq := repeat
  (match goal with
  | SH: [_, _ #; _] STMT>> _ |- _ => next_with SH
  end).

Ltac do_eval := repeat
  (match goal with
  | EH: [_, _] EXPR>> _ |- _ => next_with EH
  end).

Tactic Notation "next" constr(st') :=
  match goal with
  | SH: [_, _] STMT>> st' |- _ => next_with SH; do_eval
  end.

The `unseq` tactic will unfold any sequences into separate premises, and the
`next` tactic takes a final state that will destruct the specific statement that
converges to the state specified:

Theorem conv_ex3: forall st,
  [fun _ => 0,
    (* S1 *) "a" #= #2 #;
    (* S2 *) "b" #= #2 #;
    (* S3 *) "x" #= #0 #;
    (* S4 *) WHILE %"b" #!= #0 DO
    (* S5 *)   "x" #= %"x" #+ %"a" #;
    (* S6 *)   "b" #= %"b" #- #1
    DONE] STMT>> st -> st "x" = 4.

'''

ind_prop_checks = [
check_header + '''
Import Simpl.
Require Import Coq.Strings.String.
Open Scope string_scope.
Check SimplChall.conv_ex1:
  [update (update (fun _ => 0) "a" 2) "b" 3,
   #23 #+ %"a" #* %"b" #- (#1 #== #0)] EXPR>> 29.
''',
check_header + '''
Import Simpl.
Require Import Coq.Strings.String.
Open Scope string_scope.
Check SimplChall.conv_ex2: forall st,
  [fun _ => 0,
    "a" #= #1 #+ #2 #;
    "b" #= %"a" #+ #1] STMT>> st -> st "b" = 4.
''',
check_header + '''
Import Simpl.
Require Import Coq.Strings.String.
Open Scope string_scope.
Check SimplChall.conv_ex3: forall st,
  [fun _ => 0,
    (* S1 *) "a" #= #2 #;
    (* S2 *) "b" #= #2 #;
    (* S3 *) "x" #= #0 #;
    (* S4 *) WHILE %"b" #!= #0 DO
    (* S5 *)   "x" #= %"x" #+ %"a" #;
    (* S6 *)   "b" #= %"b" #- #1
    DONE] STMT>> st -> st "x" = 4.
''',
]

tut_final = '''
Okay now that you have some practice. Let's go back to my original proofs. Now
we are trying to prove stuff not just specific programs, but about some general
set of programs!
'''
