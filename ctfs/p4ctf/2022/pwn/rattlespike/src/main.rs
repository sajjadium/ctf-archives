use std::fs::File;
use std::io::BufWriter;
use std::path::Path;

fn main() {
    let mut args = std::env::args();
    let _ = args.next().unwrap();
    match args.next().unwrap().as_str() {
        "run" => {
            let filename = args.next().unwrap();
            let source = std::fs::read_to_string(&filename).unwrap();
            let _ = rattlespike::run(source, filename);
        }
        "compile" => {
            let filename = args.next().unwrap();
            let outfile = args.next().unwrap();
            let source = std::fs::read_to_string(&filename).unwrap();
            let _ = rattlespike::compile(source, filename, Path::new(&outfile));
        }
        "translate" => {
            let filename = args.next().unwrap();
            let outfile = args.next().unwrap();
            let outfile = File::create(outfile).unwrap();
            let outfile = BufWriter::new(outfile);
            let source = std::fs::read_to_string(&filename).unwrap();
            let _ = rattlespike::compile_to_c(source, filename, outfile);
        }
        cmd => eprintln!("Unknown subcommand {cmd:?}"),
    }
}
