#lang falsch
;; Falsch is a theorem prover based on rewriting of a pure Lisp dialect, largely
;; inspired by ACL2 and J-Bob. Since it's written in Racket, the DrRacket IDE
;; already supports Falsch. Just run
;; $ raco pkg install ./falsch
;; $ drracket tutorial.rkt

;; Let's prove a simple theorem.
(defthm (test)
  (equal? (cons 'a 'b) '(a . b)))
;; The output will look like this:
; Goal:
; (equal? (cons 'a 'b) '(a . b))

;; We can apply a builtin function with
(-> (1) (cons 'a 'b))
;; The (1) is the path — it says we would like to focus on the first argument of equal?
; Goal:
; (equal? '(a . b) '(a . b))

;; Now we would like to rewrite the entire expression, so the path is empty:
(-> () (equal? '(a . b) '(a . b)))
; Goal:
; #t

;; Looks like our proof was successful. Let's celebrate:
(qed)

;; This is not the only way to prove this.
(defthm (test2)
  (equal? (cons 'a 'b) '(a . b)))
; Goal:
; (equal? (cons 'a 'b) '(a . b))

;; This time, let's apply the equality in the other direction.
(<- (2) (cons 'a 'b))
; Goal:
; (equal? (cons 'a 'b) (cons 'a 'b))

;; This time, the arguments to equal? aren't literals, so we can't just execute
;; it. We will use an axiom, equal-same.
;;
;; (defaxiom (equal-same x)
;;   (equal? (equal? x x) #t))
;;
;; We need the instance of this axiom where x is (cons 'a 'b), so...
(-> () (equal-same (cons 'a 'b)))
; Goal:
; #t

;; Done again. Proofs are easy.
(qed)

;; Let's define a function.
(defun (id x)
  (if (cons? x)
      (cons (car x) (cdr x))
      x))

;; Like the name suggests, this is a convoluted way of writing the identity
;; function. We can prove that this is the case:
(defthm (equal/id x)
  (equal? (id x) x))
; Goal:
; (equal? (id x) x)

(-> (1) (id x))
; Goal:
; (equal? (if (cons? x) (cons (car x) (cdr x)) x) x)

;; To focus into an if, we use the following names: (if Q A E). They stand for
;; question, answer, and else, respectively.
(-> (1 A) (cons/car+cdr x))
; Goal:
; (equal? (if (cons? x) x x) x)

(-> (1) (if-same (cons? x) x))
; Goal:
; (equal? x x)

(-> () (equal-same x))
; Goal:
; #t

(qed)

;; This proof required some more axioms. You can see a full list of available
;; axioms at the end of main.rkt. Now, let the challenge begin.

(get-flag)
; Goal:
; #f
