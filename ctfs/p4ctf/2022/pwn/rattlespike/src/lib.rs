use codemap::{CodeMap, File};
use codemap_diagnostic::{ColorConfig, Emitter};
use std::io::prelude::*;
use std::io::BufWriter;
use std::path::Path;
use std::process::Command;
use tempfile::NamedTempFile;

mod ast;
mod classify;
mod emit;
mod errors;
mod parser;
mod pretty;
mod resolve;
mod verify;

pub(crate) use errors::ErrorSink;

fn do_compile(e: &mut ErrorSink, file: &File, output: impl Write) -> Result<(), ()> {
    let ast = parser::parse(e, file);
    e.may_continue()?;
    let ast = ast.unwrap();

    let ast = verify::verify(e, ast);
    e.may_continue()?;
    let ast = ast.unwrap();

    let blocks = resolve::resolve(e, &ast);
    e.may_continue()?;

    emit::emit(&blocks, &ast.characters, output).unwrap();

    Ok(())
}

pub fn compile_to_c(input: String, filename: String, output: impl Write) -> Result<(), ()> {
    let mut codemap = CodeMap::new();
    let file = codemap.add_file(filename, input);
    let mut e = ErrorSink::new();

    let ok = do_compile(&mut e, &file, output);

    let mut emitter = Emitter::stderr(ColorConfig::Always, Some(&codemap));
    for diagnostic in e.diagnostics {
        emitter.emit(&[diagnostic]);
    }

    ok
}

pub fn compile(input: String, filename: String, output_path: &Path) -> Result<(), ()> {
    let mut file = NamedTempFile::new().unwrap();
    let output = BufWriter::new(&mut file);
    compile_to_c(input, filename, output)?;

    let exited = Command::new("gcc")
        .args(["-O2", "-x", "c"])
        .arg(file.path().as_os_str())
        .arg("-o")
        .arg(output_path)
        .status()
        .unwrap();

    if !exited.success() {
        eprintln!("Failed to compile C code");
        return Err(());
    }

    Ok(())
}

pub fn run(input: String, filename: String) -> Result<(), ()> {
    let output_path = NamedTempFile::new().unwrap().into_temp_path();
    compile(input, filename, &output_path)?;

    Command::new(&output_path)
        .status()
        .unwrap();

    Ok(())
}
