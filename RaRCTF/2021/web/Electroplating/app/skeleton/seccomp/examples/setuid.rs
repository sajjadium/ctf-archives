extern crate libc;
extern crate seccomp;

use seccomp::*;

fn main() {
    let mut ctx = Context::default(Action::Allow).unwrap();
    let rule = Rule::new(
        105, /* setuid on x86_64 */
        Compare::arg(0).with(1000).using(Op::Eq).build().unwrap(),
        Action::Errno(libc::EPERM), /* return EPERM */
    );
    ctx.add_rule(rule).unwrap();
    ctx.load().unwrap();
    let ret = unsafe { libc::setuid(1000) };
    println!("ret = {}, uid = {}", ret, unsafe { libc::getuid() });
}
