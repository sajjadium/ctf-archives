use pyo3::prelude::*;
use pyo3::types::PyDict;
use seccomp_sys::{
    seccomp_init, seccomp_load, seccomp_rule_add_array, SCMP_ACT_ALLOW, SCMP_ACT_KILL,
};
use std::io::prelude::*;

const BLOCKED_SYSCALLS: [i32; 3] = [0, 17, 19];

fn sandbox() -> Result<(), ()> {
    unsafe {
        let ctx = seccomp_init(SCMP_ACT_ALLOW);
        if ctx.is_null() {
            return Err(());
        }
        let mut status = BLOCKED_SYSCALLS
            .iter()
            .map(|syscall| seccomp_rule_add_array(ctx, SCMP_ACT_KILL, *syscall, 0, [].as_ptr()))
            .fold(0i32, |sum, val| sum | val);
        status |= seccomp_load(ctx);
        if status != 0 {
            return Err(());
        }
        Ok(())
    }
}

fn run(stream: &mut (impl Read + BufRead)) -> Result<(), ()> {
    println!("How many modules do you need to load?");
    let library_length = {
        let mut lib_len_str = String::with_capacity(2);
        stream.read_line(&mut lib_len_str).unwrap();
        lib_len_str.trim().parse::<i32>().unwrap()
    };
    let gil = Python::acquire_gil();
    let py = gil.python();
    println!("Please enter required modules, one to a line");
    let modules: Vec<(String, &PyModule)> = (0..library_length)
        .map(|_| {
            let mut temp_lib_str = String::new();
            stream.read_line(&mut temp_lib_str).unwrap();
            temp_lib_str.trim().to_string()
        })
        .filter_map(|x| {
            let module = py.import(&x);
            if module.is_err() {
                println!("Failed to import module: {}", x);
                None
            } else {
                Some((x.clone(), module.unwrap()))
            }
        })
        .collect();
    println!("Please enter code, terminated by an empty line with a period (.)");
    let code = {
        let mut temp_str = String::new();
        for line in stream.lines() {
            let line = line.unwrap();
            if line.trim() == "." {
                break
            }
            temp_str += &line;
            temp_str += &"\n";
        }
        temp_str
    };
    let mut globals = PyDict::new(py);
    let builtins = py.import("builtins");
    if builtins.is_err() {
        println!("Couldn't import builtins, probably go tell an admin");
    }
    globals.set_item("__builtins__", builtins.unwrap()).unwrap();
    modules.iter().for_each(|(name, x)| globals.set_item(name, x).unwrap());
    if let Err(_) = sandbox() {
        println!("Failed to setup sandbox");
        return Err(());
    }
    if let Err(e) = py.run(&code, Some(globals), None) {
        e.print(py);
    };

    Ok(())
}

fn main() -> Result<(), ()> {
    let stdin = std::io::stdin();

    run(&mut stdin.lock()).unwrap();
    Ok(())
}
