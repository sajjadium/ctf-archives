use dynasmrt::{
    dynasm,
    x64::{Assembler, X64Relocation},
    DynamicLabel, DynasmApi, DynasmError, DynasmLabelApi,
};

use std::fs::File;
use std::io::{BufRead, Read, Write};
use std::mem;

#[derive(Clone, Copy, Debug)]
#[repr(i8)]
enum RunResult {
    Success,
    TapeOverflow,
    TapeUnderflow,
}

fn generate_forward_labels(
    ops: &mut Assembler,
    program: &[u8],
) -> Vec<(DynamicLabel, DynamicLabel)> {
    program
        .into_iter()
        .copied()
        .filter(|&c| c == b'[')
        .map(|_| {
            let start_label = ops.new_dynamic_label();
            let end_label = ops.new_dynamic_label();
            (start_label, end_label)
        })
        .collect()
}

fn generate_jit<R: DynasmLabelApi<Relocation = X64Relocation>>(
    ops: &mut R,
    program: &[u8],
    tape: &mut [u8],
    mut forward_labels: Vec<(DynamicLabel, DynamicLabel)>,
    backward_labels: &mut Vec<(DynamicLabel, DynamicLabel)>,
) {
    dynasm!(ops
        ; .arch x64
        ; push rbx
        ; mov rcx, QWORD tape.as_mut_ptr() as _
        ; xor rbx, rbx
    );

    for c in program {
        match c {
            b'+' => dynasm!(ops
                ; .arch x64
                ; inc BYTE rcx => u8[rbx]
            ),
            b'-' => dynasm!(ops
                ; .arch x64
                ; dec BYTE rcx => u8[rbx]
            ),
            b'>' => dynasm!(ops
                ; .arch x64
                ; inc rbx
                ; mov rdx, QWORD tape.len() as _
                ; cmp rbx, rdx
                ; jl >no_overflow
                ; mov al, RunResult::TapeOverflow as i8
                ; jmp >exit
                ; no_overflow:
            ),
            b'<' => dynasm!(ops
                ; .arch x64
                ; dec rbx
                ; cmp rbx, 0
                ; jge >no_overflow
                ; mov al, RunResult::TapeUnderflow as i8
                ; jmp >exit
                ; no_overflow:
            ),
            b',' => dynasm!(ops
                ; .arch x64
                ; push rax
                ; push rcx
                ; push rdx
                ; push rdi
                ; push rsi

                ; xor rax, rax
                ; xor rdi, rdi
                ; lea rsi, rcx => u8[rbx]
                ; mov rdx, 1
                ; syscall

                ; pop rsi
                ; pop rdi
                ; pop rdx
                ; pop rcx
                ; pop rax
            ),
            b'.' => dynasm!(ops
                ; .arch x64
                ; push rax
                ; push rcx
                ; push rdx
                ; push rdi
                ; push rsi

                ; mov rax, 1
                ; mov rdi, 1
                ; lea rsi, rcx => u8[rbx]
                ; mov rdx, 1
                ; syscall

                ; pop rsi
                ; pop rdi
                ; pop rdx
                ; pop rcx
                ; pop rax
            ),
            b'[' => {
                let (forward_label, backward_label) =
                    forward_labels.pop().expect("unexpected opening bracket");
                dynasm!(ops
                    ; .arch x64
                    ; cmp BYTE rcx => u8[rbx], 0
                    ; je DWORD =>forward_label
                    ; =>backward_label
                );
                backward_labels.push((forward_label, backward_label));
            }
            b']' => {
                let (forward_label, backward_label) =
                    backward_labels.pop().expect("unmatched closing bracket");

                dynasm!(ops
                    ; .arch x64
                    ; cmp BYTE rcx => u8[rbx], 0
                    ; jne DWORD =>backward_label
                    ; =>forward_label
                )
            }
            _ => dynasm!(ops
                ; .arch x64
                ; nop
            ),
        };
    }

    dynasm!(ops
        ; .arch x64
        ; mov al, RunResult::Success as i8
        ; exit:
        ; pop rbx
        ; ret
    );
}

fn read_program() -> Vec<u8> {
    let stdin = std::io::stdin();

    print!("program length: ");
    std::io::stdout().flush().unwrap();

    let mut length_string = String::new();
    stdin
        .read_line(&mut length_string)
        .expect("failed to read length string");

    let length = length_string
        .trim()
        .parse::<usize>()
        .expect("invalid length string");
    let mut result = vec![0; length];

    print!("program source: ");
    std::io::stdout().flush().unwrap();

    stdin
        .lock()
        .read_exact(&mut result)
        .expect("failed to read program input");

    result
}

fn main() {
    let program = read_program();

    let mut ops = Assembler::new().unwrap();
    let start = ops.offset();

    let mut tape: [u8; 0x1000] = [0; 0x1000];

    let mut backward_labels = Vec::new();

    let program = program.clone();
    let forward_labels = generate_forward_labels(&mut ops, &program);

    generate_jit(
        &mut ops,
        &program,
        &mut tape,
        forward_labels,
        &mut backward_labels,
    );

    let mut result = ops.commit();

    while result.is_err() {
        println!("error assembling: {:?}", result);
        println!("please provide another (shorter or equally long) program");
        let program = read_program();

        let forward_labels = generate_forward_labels(&mut ops, &program);

        result = ops.alter(|modifier| {
            generate_jit(
                modifier,
                &program,
                &mut tape,
                forward_labels,
                &mut backward_labels,
            );
        })
    }

    {
        let reader = ops.reader();
        let buf = reader.lock();
        let f: extern "sysv64" fn() -> RunResult = unsafe { mem::transmute(buf.ptr(start)) };

        let result = f();

        println!("{:?}", result);
    }
}
