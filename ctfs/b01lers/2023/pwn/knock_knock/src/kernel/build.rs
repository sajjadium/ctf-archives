use std::env;
use std::process::Command;

const ASM_DIR: &str = "src/arch/x64";
const ASM_INCL_DIR: &str = "src/arch/x64/include";

#[cfg(not(target_arch = "x86_64"))]
fn asm_file(file: &str, out_dir: &str) {}

#[cfg(not(target_arch = "x86_64"))]
fn asm(out_dir: &str) {}

#[cfg(target_arch = "x86_64")]
fn asm_file(file: &str, out_dir: &str) {
    let file = format!("{}/{}", ASM_DIR, file);
    let out_name = file.replace('/', "-");
    let out_file = format!("lib{}.a", out_name);
    println!("cargo:rerun-if-changed={}", file);

    let status = if env::var("DEBUG").unwrap() == "true" {
        Command::new("nasm")
            .arg(file)
            .arg("-o")
            .arg(format!("{}/{}", out_dir, out_file))
            .arg(format!("-I{}", ASM_INCL_DIR))
            .arg("-g")
            .arg("-f")
            .arg("elf64")
            .arg("-F")
            .arg("Dwarf")
            .status()
            .expect("couldn't run nasm")
    } else {
        Command::new("nasm")
            .arg(file)
            .arg("-o")
            .arg(format!("{}/{}", out_dir, out_file))
            .arg(format!("-I{}", ASM_INCL_DIR))
            .arg("-f")
            .arg("elf64")
            .arg("-F")
            .arg("Dwarf")
            .status()
            .expect("couldn't run nasm")
    };

    if !status.success() {
        panic!("nasm failed with {}", status);
    }

    println!("cargo:rustc-link-lib=static={}", out_name);
}

#[cfg(target_arch = "x86_64")]
fn asm(out_dir: &str) {
    let incl_files = vec!["asm_def.asm"];

    let files = vec![
        "boot/boot.asm",
        "boot/long_init.asm",
        "boot/ap_boot.asm",
        "misc.asm",
        "int.asm",
        "syscall.asm",
        "sched.asm",
    ];

    for f in incl_files.iter() {
        println!("cargo:rerun-if-changed={}/{}", ASM_INCL_DIR, f);
    }

    for f in files.iter() {
        asm_file(f, out_dir);
    }
}

fn main() {
    let out_dir = env::var("OUT_DIR").unwrap();

    println!("cargo:rustc-link-search={}", out_dir);

    asm(&out_dir);
}
