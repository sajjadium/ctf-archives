use std::fs;
use std::rc::Rc;

use core::fmt::{Debug, Display};

extern crate rustyline;
use rustyline::error::ReadlineError;
use rustyline::Editor;

extern crate nom;
pub mod parser;

const FLAG1: &str = "TODO: Replace with flag here";
const FLAG2: &str = "TODO: Replace with flag here";
const COMMENT_BOL: &str = ";";

type Err<T> = Result<T, String>;

#[derive(Clone, PartialEq)]
pub enum Term_ {
    Variable(String),
    Sort(u8),
    Application(Term, Term),
    Abstraction(String, Term, Term),
    Pi(String, Term, Term),
    Flag,
}
type Term = Box<Term_>;

fn variable<S: Into<String>>(v: S) -> Term_ {
    Term_::Variable(v.into())
}
fn sort(s: u8) -> Term_ {
    Term_::Sort(s)
}
fn application<T1: Into<Term>, T2: Into<Term>>(e1: T1, e2: T2) -> Term_ {
    Term_::Application(e1.into(), e2.into())
}
fn abstraction<S: Into<String>, T1: Into<Term>, T2: Into<Term>>(x: S, t: T1, e: T2) -> Term_ {
    Term_::Abstraction(x.into(), t.into(), e.into())
}
fn pi<S: Into<String>, T1: Into<Term>, T2: Into<Term>>(x: S, a: T1, b: T2) -> Term_ {
    Term_::Pi(x.into(), a.into(), b.into())
}

#[derive(Clone)]
enum Env {
    Empty,
    Link(Rc<(String, Term, Option<Term>, Env)>),
}

impl Env {
    fn new() -> Self {
        Env::Empty
    }

    fn base() -> Self {
        use Term_::*;
        let mut e = Self::new();
        let easy_t = pi(
            "phi",
            sort(0),
            pi(
                "_",
                pi(
                    "_",
                    pi("_", variable("phi"), pi("p", sort(0), variable("p"))),
                    pi("p", sort(0), variable("p")),
                ),
                variable("phi"),
            ),
        );
        e.insert(
            "flag1",
            pi("x", easy_t.clone(), sort(0)),
            Some(abstraction("x", easy_t, variable(FLAG1)).into()),
        );
        e.insert(
            "flag2",
            pi("x", pi("p", sort(0), variable("p")), sort(0)),
            Some(abstraction("x", pi("p", sort(0), variable("p")), Flag).into()),
        );
        e
    }

    fn extend<S: Into<String>, T1: Into<Term>, T2: Into<Option<Term>>>(
        &self,
        v: S,
        ty: T1,
        va: T2,
    ) -> Self {
        Env::Link(Rc::new((v.into(), ty.into(), va.into(), self.clone())))
    }

    fn insert<S: Into<String>, T1: Into<Term>, T2: Into<Option<Term>>>(
        &mut self,
        v: S,
        ty: T1,
        va: T2,
    ) {
        *self = self.extend(v, ty, va);
    }

    fn get_type(&self, v: &str) -> Option<&Term> {
        match self {
            Env::Empty => None,
            Env::Link(k) => {
                let (x, t, _, l) = k.as_ref();
                if x == v {
                    Some(t)
                } else {
                    l.get_type(v)
                }
            }
        }
    }

    fn get_value(&self, v: &str) -> Option<&Term> {
        match self {
            Env::Empty => None,
            Env::Link(k) => {
                let (x, _, va, l) = k.as_ref();
                if x == v {
                    va.as_ref()
                } else {
                    l.get_value(v)
                }
            }
        }
    }

    fn contains_key(&self, v: &str) -> bool {
        match self {
            Env::Empty => false,
            Env::Link(k) => {
                let (x, _, _, l) = k.as_ref();
                if x == v {
                    true
                } else {
                    l.contains_key(v)
                }
            }
        }
    }
}

impl Iterator for Env {
    type Item = (String, Term, Option<Term>);
    fn next(&mut self) -> Option<Self::Item> {
        let mut replace = None;
        let result = match self {
            Env::Empty => None,
            Env::Link(k) => {
                let (x, t, v, l) = k.as_ref();
                replace = Some(l.clone());
                Some((x.clone(), t.clone(), v.clone()))
            }
        };
        if let Some(r) = replace {
            *self = r;
        }
        result
    }
}

impl Term_ {
    fn body_intros(&self) -> Vec<&str> {
        fn vec_append<T>(a: Vec<T>, b: Vec<T>) -> Vec<T> {
            a.into_iter().chain(b.into_iter()).collect()
        }

        use Term_::*;
        match self {
            Variable(_) | Sort(_) | Flag => vec![],
            Application(f, x) => vec_append(f.body_intros(), x.body_intros()),
            Abstraction(x, a, b) | Pi(x, a, b) => {
                vec_append(vec![x], vec_append(a.body_intros(), b.body_intros()))
            }
        }
    }

    fn scope_free_var(&self, x: &str, env: &Env) -> (String, Self) {
        let bi = self.body_intros();
        let mut new_x = x.to_string();
        while env.contains_key(&new_x) || bi.iter().any(|&x| x == new_x) {
            new_x.push('\'');
        }
        let t = self.clone();
        if x != new_x {
            (new_x.clone(), t.replace(x, &variable(new_x)))
        } else {
            (new_x, t)
        }
    }

    fn beta_normal_in(&self, env: &Env) -> Err<Self> {
        use Term_::*;
        match self {
            Variable(x) => env
                .get_value(x)
                .map_or_else(|| Ok(self.clone()), |x| x.beta_normal_in(env)),
            Sort(_) => Ok(self.clone()),
            Application(f, c) => match f.beta_normal_in(env) {
                Ok(Abstraction(x, _, e)) => e.replace(&x, c).beta_normal_in(env),
                Ok(t) => Ok(application(t, c.beta_normal_in(env)?)),
                Err(e) => Err(format!(
                    "Failure when normalizing during application: {}",
                    e
                )),
            },
            Abstraction(x, t, e) => {
                let (x1, e1) = e.scope_free_var(x, env);
                let env2 = env.extend(x1.clone(), t.beta_normal_in(env)?, None);
                assert!(
                    abstraction(x, t.clone(), e.clone()).alpha_equivalent(&abstraction(
                        x1.clone(),
                        t.clone(),
                        e1.clone()
                    )),
                    "scoping free var for `{}` does not lead to alpha equivalent. got {} instead",
                    abstraction(x, t.clone(), e.clone()),
                    abstraction(x1.clone(), t.clone(), e1.clone())
                );
                Ok(abstraction(
                    x1,
                    t.beta_normal_in(env).map_err(|e| {
                        format!("Failure in normalizing type in abstraction: {}", e)
                    })?,
                    e1.beta_normal_in(&env2).map_err(|e| {
                        format!("Failure in normalizing body in abstraction: {}", e)
                    })?,
                ))
            }
            Pi(x, a, b) => {
                let (x1, b1) = b.scope_free_var(x, env);
                let env2 = env.extend(x1.clone(), a.beta_normal_in(env)?, None);
                assert!(
                    pi(x, a.clone(), b.clone()).alpha_equivalent(&pi(
                        x1.clone(),
                        a.clone(),
                        b1.clone()
                    )),
                    "scoping free var for `{}` does not lead to alpha equivalent. got {} instead",
                    pi(x, a.clone(), b.clone()),
                    pi(x1.clone(), a.clone(), b1.clone())
                );
                Ok(pi(
                    x1,
                    a.beta_normal_in(env)
                        .map_err(|e| format!("Failure in normalizing type in pi: {}", e))?,
                    b1.beta_normal_in(&env2)
                        .map_err(|e| format!("Failure in normalizing body in pi: {}", e))?,
                ))
            }
            Flag => Ok(self.clone()),
        }
    }

    fn replace(self, xx: &str, ee: &Self) -> Self {
        use Term_::*;
        match self {
            Variable(x) if x == xx => ee.clone(),
            Variable(_) | Sort(_) => self,
            Application(f, x) => application(f.replace(xx, ee), x.replace(xx, ee)),
            Abstraction(x, t, e) => {
                let e = if x == xx { e } else { e.replace(xx, ee).into() };
                abstraction(x, t.replace(xx, ee), e)
            }
            Pi(x, a, b) => {
                let b = if x == xx { b } else { b.replace(xx, ee).into() };
                pi(x, a.replace(xx, ee), b)
            }
            Flag => self,
        }
    }

    fn compute_type(&self, env: &Env) -> Err<Self> {
        use Term_::*;

        fn aux(t: &Term_, env: &Env) -> Err<Term_> {
            match t {
                Variable(x) => env.get_type(x).map_or_else(
                    || Err(format!("Trying to use unknown variable `{}`", x)),
                    |tx| Ok(*tx.clone()),
                ),
                Sort(n) => Ok(sort(n + 1)),
                Application(ff, xx) => match ff.compute_type(env) {
                    Ok(Pi(x, a, b)) => match xx.compute_type(env) {
                        Ok(tx) => {
                            if a.alpha_equivalent(&tx) {
                                Ok(b.replace(&x, xx))
                            } else {
                                Err(format!(
                                    "Trying to apply function with wrong argument type.\
                                     \n\tReceived:\n\t\t`{}`\n\tof type\n\t\t`{}`\
                                     \n\tExpected:\n\t\t`{}`",
                                    xx.prettify_in(env),
                                    tx.prettify_in(env),
                                    a.prettify_in(env)
                                ))
                            }
                        }
                        Err(e) => Err(format!(
                            "Failure when type checking argument during application: {}",
                            e
                        )),
                    },
                    Ok(fft) => Err(format!(
                        "Trying to pass non-pi `{}` of type `{}` for function application",
                        ff, fft
                    )),
                    Err(e) => Err(format!(
                        "Failure when type checking during application: {}",
                        e
                    )),
                },
                Abstraction(x, a, b) => match a.compute_type(env) {
                    Ok(Sort(_s1)) => {
                        let (x, b) = b.scope_free_var(x, env);
                        let env2 = env.extend(&x, a.beta_normal_in(env)?, None);
                        let tb = b.compute_type(&env2).or_else(|e| {
                            Err(format!("Failure in computing type of body: {}", e))
                        })?;
                        match tb.compute_type(&env2) {
                            Ok(Sort(_s2)) => Ok(pi(x, a.clone(), tb)),
                            Ok(ttb) => Err(format!("Got non-sort type `{}` for `{}`", ttb, tb)),
                            Err(e) => Err(format!("Failure in computing sort of body: {}", e)),
                        }
                    }
                    Ok(ta) => Err(format!("Got non-sort type `{}` for `{}`", ta, a)),
                    Err(e) => Err(format!("Failure in computing sort of parameter: {}", e)),
                },
                Pi(x, a, b) => match a.compute_type(env) {
                    Ok(Sort(_s1)) => {
                        let (x, b) = b.scope_free_var(x, env);
                        let env2 = env.extend(&x, a.beta_normal_in(env)?, None);
                        match b.compute_type(&env2) {
                            Ok(Sort(s2)) => Ok(sort(s2)),
                            Ok(t) => Err(format!(
                                "For second sort for pi, got non-sort for `{}`: `{}`",
                                b, t
                            )),
                            Err(e) => {
                                Err(format!("Unable to compute valid second sort for pi: {}", e))
                            }
                        }
                    }
                    Ok(t) => Err(format!(
                        "For first sort for pi, got non-sort for `{}`: `{}`",
                        a, t
                    )),
                    Err(e) => Err(format!("Unable to compute valid first sort for pi: {}", e)),
                },
                Flag => Ok(Sort(0)),
            }
        }

        aux(self, env).and_then(|x| x.beta_normal_in(env))
    }

    fn alpha_equivalent(&self, other: &Self) -> bool {
        use Term_::*;
        match (self, other) {
            (Variable(x1), Variable(x2)) => x1 == x2,
            (Sort(s1), Sort(s2)) => s1 == s2,
            (Application(f1, x1), Application(f2, x2)) => {
                f1.alpha_equivalent(f2) && x1.alpha_equivalent(x2)
            }
            (Abstraction(x1, t1, e1), Abstraction(x2, t2, e2)) => {
                t1.alpha_equivalent(t2)
                    && e1.alpha_equivalent(&e2.clone().replace(x2, &variable(x1)))
            }
            (Pi(x1, a1, b1), Pi(x2, a2, b2)) => {
                a1.alpha_equivalent(a2)
                    && b1.alpha_equivalent(&b2.clone().replace(x2, &variable(x1)))
            }
            (Flag, Flag) => true,
            _ => false,
        }
    }

    fn prettify_in(&self, env: &Env) -> Self {
        use Term_::*;

        if let Variable(_) = self {
            return self.clone();
        }
        for (k, _, v) in env.clone() {
            if let Some(v) = v {
                if self.alpha_equivalent(&v) {
                    return variable(k);
                }
            }
        }
        match self {
            Variable(_) => unreachable!(),
            Sort(_) => self.clone(),
            Application(f, x) => application(f.prettify_in(env), x.prettify_in(env)),
            Abstraction(x, t, e) => abstraction(x, t.prettify_in(env), e.prettify_in(env)),
            Pi(x, a, b) => pi(x, a.prettify_in(env), b.prettify_in(env)),
            Flag => Flag,
        }
    }
}

impl Display for Term_ {
    fn fmt(&self, f: &mut core::fmt::Formatter) -> Result<(), core::fmt::Error> {
        use Term_::*;

        fn aux(
            t: &Term_,
            f: &mut core::fmt::Formatter,
            in_parens: bool,
        ) -> Result<(), core::fmt::Error> {
            match t {
                Variable(x) => write!(f, "{}", x),
                Sort(n) => write!(f, "#{}", n),
                Application(ff, xx) => {
                    if !in_parens {
                        write!(f, "(")?;
                    }
                    aux(ff, f, true)?;
                    write!(f, " ")?;
                    aux(xx, f, false)?;
                    if !in_parens {
                        write!(f, ")")?;
                    }
                    Ok(())
                }
                Abstraction(x, t, e) => write!(f, "({} : {}) -> {}", x, t, e),
                Pi(x, a, b) => write!(f, "({} : {}) => {}", x, a, b),
                Flag => write!(f, "FLAG"),
            }
        }

        aux(self, f, false)
    }
}

impl Debug for Term_ {
    fn fmt(&self, f: &mut core::fmt::Formatter) -> Result<(), core::fmt::Error> {
        write!(f, "[[[{}]]]", self)
    }
}

impl Display for Env {
    fn fmt(&self, f: &mut core::fmt::Formatter) -> Result<(), core::fmt::Error> {
        write!(f, "{{")?;
        for (k, t, v) in self.clone() {
            write!(f, "{} = {:?} : {}, ", k, v, t)?;
        }
        write!(f, "}}")?;
        Ok(())
    }
}

fn eval_and_print(x: Option<&str>, v: &Term, env: &mut Env) {
    match v.compute_type(&env) {
        Ok(t) => match v.beta_normal_in(&env) {
            Ok(v) => {
                if let Some(x) = &x {
                    print!("{} = ", x);
                }
                println!("({}) : {}", v.prettify_in(&env), t.prettify_in(&env));
                if v == Term_::Flag {
                    println!("Congratulations! {}", FLAG2);
                }
                if let Some(x) = x {
                    env.insert(x, t, Some(v.into()));
                }
            }
            Err(e) => {
                println!("Failed to beta reduce: {}", e);
            }
        },
        Err(e) => {
            println!("Failed to type check: {}", e);
        }
    };
    println!();
}

fn strip_comments(s: &str) -> String {
    format!(
        "{}\n", /* force extra newline */
        s.lines()
            .filter(|x| x != &"" && !x.starts_with(COMMENT_BOL))
            .collect::<Vec<&str>>()
            .join("\n")
    )
}

fn parse_eval_and_print(input: &str, env: &mut Env, print_term: bool) -> (String, bool) {
    let input = &strip_comments(input);
    let (partially_parsed, v, incomplete) = crate::parser::parse_many(input);
    for (input, name, term) in &v {
        if print_term {
            println!(">> {}", input)
        }
        eval_and_print(name.as_deref(), &term, env);
    }
    if let Err(e) = &incomplete {
        println!("{}", e);
    }
    (partially_parsed.trim_start().into(), v.len() > 0)
}

fn repl() {
    let mut env = Env::base();

    let mut args = std::env::args();
    args.next();
    if let Some(filename) = args.next() {
        if let Ok(initial_setup) = fs::read_to_string(filename) {
            let _ = parse_eval_and_print(&initial_setup, &mut env, true);
            if let None = args.next() {
                return;
            }
        } else {
            println!("Could not find file");
            return;
        }
    }

    let mut rl = Editor::<()>::new();
    let history_file = ".history";
    rl.load_history(history_file).unwrap_or_default();
    let mut partially_parsed = String::new();
    loop {
        let readline = rl.readline(if partially_parsed.is_empty() {
            ">> "
        } else {
            "   "
        });
        match readline {
            Ok(line) => {
                if line.trim() != "" {
                    rl.add_history_entry(&line);
                }
                partially_parsed.push_str(&line);
                let (p_p, any_parsed) = parse_eval_and_print(&partially_parsed, &mut env, false);
                partially_parsed = p_p;
                if any_parsed && !partially_parsed.is_empty() {
                    println!(">> {}", partially_parsed.trim_end());
                }
            }
            Err(ReadlineError::Interrupted) => {
                println!("Interrupted. Exiting.");
                break;
            }
            Err(ReadlineError::Eof) => {
                println!("EOF. Exiting.");
                break;
            }
            Err(err) => {
                println!("Error: {:?}", err);
                break;
            }
        }
    }
    rl.save_history(history_file).unwrap();
}

fn main() {
    repl();
}
