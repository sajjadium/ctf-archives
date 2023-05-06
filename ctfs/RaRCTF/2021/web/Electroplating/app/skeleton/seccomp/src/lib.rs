//! This crate is based on [seccomp_sys](https://crates.io/crates/seccomp-sys) and provides
//! a higher level wrapper for [libseccomp](https://github.com/seccomp/libseccomp).
//!
//!
//! Example usage:
//!
//! ```rust,no_run
//!extern crate seccomp;
//!extern crate libc;
//!
//!use seccomp::*;
//!
//!fn main() {
//!     let mut ctx = Context::default(Action::Allow).unwrap();
//!     let rule = Rule::new(105 /* setuid on x86_64 */,
//!         Compare::arg(0)
//!                 .with(1000)
//!                 .using(Op::Eq)
//!                 .build().unwrap(),
//!         Action::Errno(libc::EPERM) /* return EPERM */
//!     );
//!     ctx.add_rule(rule).unwrap();
//!     ctx.load().unwrap();
//!     let ret = unsafe { libc::setuid(1000) };
//!     println!("ret = {}, uid = {}", ret, unsafe { libc::getuid() });
//!}
//!# pook perd
//!

extern crate libc;
extern crate seccomp_sys;

use seccomp_sys::scmp_compare::*;
use seccomp_sys::*;
use std::convert::Into;
use std::error::Error;
use std::fmt;

pub type Cmp = scmp_arg_cmp;

/// Comparison operators
#[derive(Debug, Clone, Copy)]
pub enum Op {
    /// not equal
    Ne,
    /// less than
    Lt,
    /// less than or equal
    Le,
    /// equal
    Eq,
    /// greater than or equal
    Ge,
    /// greater than
    Gt,
    /// masked equality
    MaskedEq,
}

impl Into<scmp_compare> for Op {
    fn into(self) -> scmp_compare {
        match self {
            Op::Ne => SCMP_CMP_NE,
            Op::Lt => SCMP_CMP_LT,
            Op::Le => SCMP_CMP_LE,
            Op::Eq => SCMP_CMP_EQ,
            Op::Ge => SCMP_CMP_GE,
            Op::Gt => SCMP_CMP_GT,
            Op::MaskedEq => SCMP_CMP_MASKED_EQ,
        }
    }
}

/// Seccomp actions
#[derive(Debug, Clone, Copy)]
pub enum Action {
    /// Allow the syscall to be executed
    Allow,
    /// Kill the offending thread
    Kill,
    /// Kill the whole offending process
    KillProcess,
    /// Throw a SIGSYS signal
    Trap,
    /// Return the specified error code
    Errno(i32),
    /// Notify a tracing process with the specified value
    Trace(u32),
}

impl Into<u32> for Action {
    fn into(self) -> u32 {
        match self {
            Action::Allow => SCMP_ACT_ALLOW,
            Action::Kill => SCMP_ACT_KILL,
            Action::KillProcess => SCMP_ACT_KILL_PROCESS,
            Action::Trap => SCMP_ACT_TRAP,
            Action::Errno(x) => SCMP_ACT_ERRNO(x as u32),
            Action::Trace(x) => SCMP_ACT_TRACE(x),
        }
    }
}

/// Comparison definition builder
pub struct Compare {
    arg: libc::c_uint,
    op: Option<Op>,
    datum_a: Option<scmp_datum_t>,
    datum_b: Option<scmp_datum_t>,
}

impl Compare {
    /// argument number, starting at 0
    pub fn arg(arg_num: u32) -> Self {
        Compare {
            arg: arg_num as libc::c_uint,
            op: None,
            datum_a: None,
            datum_b: None,
        }
    }

    /// Comparison operator
    pub fn using(mut self, op: Op) -> Self {
        self.op = Some(op);
        self
    }

    /// Datum to compare with
    pub fn with(mut self, datum: u64) -> Self {
        self.datum_a = Some(datum);
        self
    }

    /// Second datum
    pub fn and(mut self, datum: u64) -> Self {
        self.datum_b = Some(datum);
        self
    }

    /// build comparison definition
    pub fn build(self) -> Option<Cmp> {
        if self.op.is_some() && self.datum_a.is_some() {
            Some(Cmp {
                arg: self.arg,
                op: self.op.unwrap().into(),
                datum_a: self.datum_a.unwrap(),
                datum_b: self.datum_b.unwrap_or(0),
            })
        } else {
            None
        }
    }
}

/// Seccomp rule
#[derive(Debug)]
pub struct Rule {
    action: Action,
    syscall_nr: usize,
    comparators: Vec<Cmp>,
}

impl Rule {
    /// Create new rule for `syscall_nr` using comparison `cmp`.
    pub fn new(syscall_nr: usize, cmp: Option<Cmp>, action: Action) -> Rule {
        Rule {
            action,
            syscall_nr,
            comparators: match cmp {
                Some(cmp) => vec![cmp],
                None => vec![]
            },
        }
    }

    /// Adds comparison. Multiple comparisons will be
    /// ANDed together.
    pub fn add_comparison(&mut self, cmp: Cmp) {
        self.comparators.push(cmp);
    }
}

/// Error type
#[derive(Debug)]
pub struct SeccompError {
    msg: String,
}

impl SeccompError {
    fn new<T: Into<String>>(msg: T) -> Self {
        SeccompError { msg: msg.into() }
    }
}

impl fmt::Display for SeccompError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "SeccompError: {}", self.msg)
    }
}

impl Error for SeccompError {
    fn description(&self) -> &str {
        &self.msg
    }
}

/// Seccomp context
#[derive(Debug)]
pub struct Context {
    int: *mut scmp_filter_ctx,
}

impl Context {
    /// Creates new context with default action
    pub fn default(def_action: Action) -> Result<Context, SeccompError> {
        let filter_ctx = unsafe { seccomp_init(def_action.into()) };
        if filter_ctx.is_null() {
            return Err(SeccompError::new("initialization failed"));
        }
        Ok(Context { int: filter_ctx })
    }

    /// Adds rule to the context
    pub fn add_rule(&mut self, rule: Rule) -> Result<(), SeccompError> {
        let res = unsafe {
            seccomp_rule_add_array(
                self.int,
                rule.action.into(),
                rule.syscall_nr as i32,
                rule.comparators.len() as u32,
                rule.comparators.as_slice().as_ptr(),
            )
        };
        if res != 0 {
            Err(SeccompError::new(format!("failed to add rule {:?}", rule)))
        } else {
            Ok(())
        }
    }

    /// Loads the filter into the kernel. Rules will be applied when this function returns.
    pub fn load(&self) -> Result<(), SeccompError> {
        let res = unsafe { seccomp_load(self.int) };
        if res != 0 {
            Err(SeccompError::new("failed to load filter into the kernel"))
        } else {
            Ok(())
        }
    }
}

impl Drop for Context {
    fn drop(&mut self) {
        unsafe { seccomp_release(self.int) }
    }
}

#[test]
fn it_works() {
    fn test() -> Result<(), Box<dyn Error>> {
        let mut ctx = Context::default(Action::Allow)?;
        ctx.add_rule(Rule::new(
            105,
            Compare::arg(0).using(Op::Eq).with(1000).build().unwrap(),
            Action::Errno(libc::EPERM),
        ))?;
        ctx.load()?;
        let ret = unsafe { libc::setuid(1000) };
        println!("ret = {}, uid = {}", ret, unsafe { libc::getuid() });
        Ok(())
    }
    test().unwrap();
}
