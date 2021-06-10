#lang racket/base
(require
  falsch/kernel
  (for-syntax racket/base))
(provide #%datum)

(define-syntax (module-begin stx)
  (syntax-case stx ()
    [(_ CMDS ...) #'(#%module-begin CMDS ... (show-goal))]))

(define-syntax (top-interaction stx)
  (syntax-case stx ()
    [(_ . CMD) #'(#%top-interaction . (begin CMD (show-goal)))]))

(provide (rename-out
          [module-begin #%module-begin]
          [top-interaction #%top-interaction]))

;; Turns (parse X) into X.
(define-for-syntax (strip-outer stx)
  (syntax-case stx ()
    [(_ X) #'X]))

;; Problem: syntax-case's literal-id list takes hygiene into account too well
;; — identifiers are considered equal iff they refer to the same definition
;; (or if neither refers to an existing definition). The symbols in a #lang falsch
;; file indeed don't refer to a definition, but in this file, if and quote *are* defined.
;;
;; If you know of a less-hacky solution, let me know!
(define-for-syntax (fixup stx)
  (define (fixup-symbol s)
    (case (syntax-e s)
      [(if) #'if]
      [(quote) #'quote]
      [else s]))
  
  (define stx-e (syntax-e stx))
  (if (list? stx-e)
      (let* ([symbol (fixup-symbol (car stx-e))]
             [new-e (cons symbol (cdr stx-e))])
        (datum->syntax stx new-e))
      stx))

(define-syntax (parse stx)
  (syntax-case (fixup (strip-outer stx)) (if quote)
    [(if Q A E) #'(If (parse Q) (parse A) (parse E))]
    [(if . _)
     (raise-syntax-error 'parse "wrong number of arguments for if expression")]
    [(quote X) #'(Lit 'X)]
    [(quote . _)
     (raise-syntax-error 'parse "wrong number of arguments for quote")]
    [(F ARG ...) #'(App 'F (list (parse ARG) ...))]
    [X
     (let ([datum (syntax->datum #'X)])
       (if (symbol? datum)
           #'(Var 'X)
           #'(Lit X)))]))

(define-syntax (defun stx)
  (syntax-case stx ()
    [(_ (F ARG ...) BODY)
     #'(handle-defun 'F '(ARG ...) (parse BODY))]))

(define-syntax (defthm stx)
  (syntax-case stx ()
    [(_ (F ARG ...) BODY)
     #'(handle-defthm 'F '(ARG ...) (parse BODY))]))

(define-for-syntax (rewrite-macro stx)
  (syntax-case stx ()
    [(DIR PATH (NAME ARGS ...))
     #'(rewrite 'DIR 'PATH 'NAME (list (parse ARGS) ...))]))

(define-syntax -> rewrite-macro)
(define-syntax <- rewrite-macro)

(define-syntax (qed stx)
  (syntax-case stx ()
    [(_) #'(handle-qed)]))

(define-syntax (get-flag stx)
  (syntax-case stx ()
    [(_) #'(flag-goal)]))

(provide defun defthm -> <- qed get-flag)

(define-syntax (defaxiom stx)
  (syntax-case stx ()
    [(_ (NAME ARGS ...) BODY)
     #'(env-insert 'NAME (Thm '(ARGS ...) (parse BODY)))]))

(defaxiom (cons?/cons x y)
  (equal? (cons? (cons x y)) #t))
(defaxiom (car/cons x y)
  (equal? (car (cons x y)) x))
(defaxiom (cdr/cons x y)
  (equal? (cdr (cons x y)) y))
(defaxiom (equal-same x)
  (equal? (equal? x x) #t))
(defaxiom (equal-swap x y)
  (equal? (equal? x y) (equal? y x)))
(defaxiom (if-same x y)
  (equal? (if x y y) y))
(defaxiom (if-true x y)
  (equal? (if #t x y) x))
(defaxiom (if-false x y)
  (equal? (if #f x y) y))
(defaxiom (if-nest-A x y z)
  (if x (equal? (if x y z) y) #t))
(defaxiom (if-nest-E x y z)
  (if x #t (equal? (if x y z) z)))
(defaxiom (cons/car+cdr x)
  (if (cons? x)
      (equal? (cons (car x) (cdr x)) x)
      #t))
(defaxiom (if/equal x y)
  (if (equal? x y)
      (equal? x y)
      #t))