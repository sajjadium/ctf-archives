#lang typed/racket
(require datatype)
(provide (all-defined-out))

(define-type Value (U Boolean Symbol (Pair Value Value) Null))

(define-datatype Expr
  [Lit (Value)]
  [Var (Symbol)]
  [App (Symbol (Listof Expr))]
  [If (Expr Expr Expr)])

(define (expr->sexp [e : Expr]) : Any
  (type-case Expr e
    [(Lit v)
     =>
     (if (boolean? v)
         v
         `',v)]
    [(Var v) => v]
    [(App f args) => (cons f (map expr->sexp args))]
    [(If q a e) => `(if ,(expr->sexp q) ,(expr->sexp a) ,(expr->sexp e))]))

(define-datatype Def
  [UnOp ((-> Value Value))]
  [BinOp ((-> Value Value Value))]
  [Thm ((Listof Symbol) Expr)])

(: env (Mutable-HashTable Symbol Def))
(define env (make-hash))

(define (env-insert [name : Symbol] [val : Def])
  (if (hash-has-key? env name)
      (error name "already exists")
      (hash-set! env name val)))
(env-insert 'equal? (BinOp equal?))
(env-insert 'cons (BinOp cons))
(env-insert 'cons? (UnOp cons?))
(env-insert 'car (UnOp (lambda (p) (if (cons? p) (car p) #f))))
(env-insert 'cdr (UnOp (lambda (p) (if (cons? p) (cdr p) #f))))

(define (subst [e : Expr] [substs : (Listof (Pair Symbol Expr))]) : Expr
  (type-case Expr e
    [(Lit x) => (Lit x)]
    [(Var v)
     =>
     (let ([subst (assoc v substs)])
       (if subst
           (cdr subst)
           (Var v)))]
    [(App f xs)
     =>
     (App f (map (lambda ([e : Expr]) (subst e substs))
                 xs))]
    [(If q a e)
     =>
     (If (subst q substs)
         (subst a substs)
         (subst e substs))]))

(define (check-recursion [name : Symbol] [e : Expr] [tail : Boolean]) : Void
  (type-case Expr e
    [(Lit x) => (void)]
    [(Var x) => (void)]
    [(App f xs)
     =>
     (cond
       [(equal? name f)
        (unless tail
          (error name "recursive call must be in tail position"))]
       [(hash-has-key? env f) (void)]
       [else (error name "unknown procedure ~a" f)])
     (for-each
      (lambda ([e : Expr])
        (check-recursion name e #f))
      xs)]
    [(If q a e)
     =>
     (check-recursion name q #f)
     (check-recursion name a tail)
     (check-recursion name e tail)]))

(define (handle-defun [name : Symbol] [args : (Listof Symbol)] [body : Expr])
  (check-recursion name body #t)
  (define thm (App 'equal? (list (App name (map Var args)) body)))
  (env-insert name (Thm args thm)))

(: goal (U False Expr))
(define goal #f)

(: on-qed (-> Any))
(define on-qed void)

(define (show-goal)
  (let ([goal goal]) ; typechecker wants this ¯\_(ツ)_/¯
    (when goal
      (display "Goal:\n")
      (pretty-write (expr->sexp goal)))))

(define (handle-qed)
  (cond
    [(not goal) (error 'qed "no active goal")]
    [(equal? goal (Lit #t))
     (on-qed)
     (set! goal #f)]
    [else (error 'qed "proof not finished")]))

(define (handle-defthm [name : Symbol] [args : (Listof Symbol)] [body : Expr])
  (set! goal body)
  (set! on-qed
        (lambda ()
          (env-insert name (Thm args body)))))

(define-type Path (Listof (U 'Q 'A 'E Positive-Integer)))
(define-type Assumptions (Listof (Pair Expr Boolean)))

(define (focus [path : Path] [ass : Assumptions] [e : Expr] [f : (-> Assumptions Expr Expr)]) : Expr
  (if (empty? path)
      (f ass e)
      (type-case Expr e
        [(Lit _) => (error 'focus "cannot focus into a literal")]
        [(Var _) => (error 'focus "cannot focus into a variable")]
        [(App fn args)
         =>
         (if (symbol? (car path))
             (error 'focus "cannot focus into a ~a call with ~a" fn (car path))
             (App fn (list-update args (sub1 (car path))
                                  (lambda ([e : Expr])
                                    (focus (cdr path) ass e f)))))]
        [(If q a e)
         =>
         (case (car path)
           [(Q) (If (focus (cdr path) ass q f) a e)]
           [(A) (If q (focus (cdr path) (cons (cons q #t) ass) a f) e)]
           [(E) (If q a (focus (cdr path) (cons (cons q #f) ass) e f))]
           [else (error 'focus "cannot focus into an if with ~a" (car path))])])))

(define (lit [e : Expr])
  (type-case Expr e
    [(Lit e) => e]
    [else => (error "primitives can only be applied to literals")]))

(define (arity [def : Def])
  (type-case Def def
    [(UnOp _) => 1]
    [(BinOp _) => 2]
    [(Thm args _) => (length args)]))

(define (apply-def [name : Symbol] [args : (Listof Expr)])
  (define def (hash-ref env name))
  (define (equal-to [v : Value])
    (App 'equal? (list (App name args) (Lit v))))
  (unless (equal? (length args) (arity def))
    (error "arity mismatch"))
  (type-case Def def
    [(UnOp f) => (equal-to (f (lit (first args))))]
    [(BinOp f) => (equal-to (f (lit (first args)) (lit (second args))))]
    [(Thm formal body) => (subst body (map (inst cons Symbol Expr) formal args))]))

(define (resolve-assumptions [ass : Assumptions] [e : Expr]) : Expr
  (type-case Expr e
    [(If q a e)
     =>
     (let ([assm (assoc q ass)])
       (cond
         [(not assm) (error 'rewrite "unresolved assumption: ~s" (expr->sexp q))]
         [(cdr assm) (resolve-assumptions ass a)]
         [else       (resolve-assumptions ass e)]))]
    [else => e]))

(define (equality [e : Expr]) : (Pair Expr Expr)
  (type-case Expr e
    [(App f args)
     =>
     (unless (equal? f 'equal?)
       (error 'rewrite "not an equality: ~s" (expr->sexp e)))
     (match args
       [(list L R) (cons L R)]
       [else (error 'rewrite "arity mismatch: ~s" (expr->sexp e))])]
    [else => (error 'rewrite "not an equality: ~s" (expr->sexp e))]))

(define-type Dir (U '-> '<-))
(define (eq-dir [dir : Dir] [eq : (Pair Expr Expr)])
  (case dir
    [(->) eq]
    [(<-) (cons (cdr eq) (car eq))]))

(define (rewrite [dir : Dir] [path : Path] [name : Symbol] [args : (Listof Expr)])
  (let ([thm (apply-def name args)]
        [g goal])
    (unless g
      (error 'rewrite "no pending goal"))
    (set! goal (focus path empty g
                      (lambda (ass e)
                        (let* ([eq (resolve-assumptions ass thm)]
                               [lr (equality eq)]
                               [from-to (eq-dir dir lr)]
                               [from (car from-to)]
                               [to (cdr from-to)])
                          (unless (equal? from e)
                            (error 'rewrite "cannot rewrite ~s — expected ~s" (expr->sexp e) (expr->sexp from)))
                          to))))))

(define (flag-goal)
  (set! goal (Lit #f))
  (set! on-qed
        (lambda ()
          (display "TODO: put flag here"))))