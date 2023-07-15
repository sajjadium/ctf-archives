use church::Graph;
use std::{io, io::Write};

fn read_graph(lines: &mut impl Iterator<Item = String>) -> Graph {
    let n = lines.next().unwrap().parse::<usize>().unwrap();

    Graph::new(
        lines
            .take(n)
            .map(|l| {
                l.chars()
                    .map(|c| match c {
                        '0' => false,
                        '1' => true,
                        _ => unreachable!(),
                    })
                    .collect()
            })
            .collect(),
    )
}

fn print_pilgrimages(p: &[Vec<usize>]) {
    let mut buf = vec![];

    for c in p {
        writeln!(
            buf,
            "{}",
            c.iter()
                .map(|x| x.to_string())
                .collect::<Vec<_>>()
                .join(" ")
        )
        .unwrap();
    }

    io::stdout().write_all(&buf).expect("io error");
    io::stdout().flush().expect("io error");
}

fn main() {
    let mut lines = io::stdin().lines().map(|l| l.expect("io error"));

    let graph = read_graph(&mut lines);

    print_pilgrimages(&church::find_pilgrimages(&graph));

    eprintln!("{}", lines.next().unwrap());
}
