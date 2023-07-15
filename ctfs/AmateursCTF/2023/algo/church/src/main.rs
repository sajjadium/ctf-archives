use church::{find_pilgrimages, Graph};
use std::io::{self, BufRead, Write};

fn print_graph(g: &Graph) {
    let n = g.n();

    let mut buf = vec![];

    writeln!(buf, "{}", n).unwrap();

    for i in 0..n {
        for j in 0..n {
            write!(buf, "{}", g.has_road(i, j) as i32).unwrap();
        }
        writeln!(buf).unwrap();
    }

    io::stdout().write_all(&buf).expect("io error");
    io::stdout().flush().expect("io error");
}

fn read_pilgrimages(g: &Graph) -> Vec<Vec<usize>> {
    let n = g.n();

    let mut ans = vec![];

    let mut stdin = io::stdin().lock();

    for _ in 0..n {
        let mut line = String::new();
        stdin.read_line(&mut line).expect("expected another line");

        let tokens = line
            .split_whitespace()
            .map(|s| s.parse::<usize>())
            .collect::<Result<Vec<_>, _>>()
            .expect("line contains non-integers");

        ans.push(tokens);
    }

    ans
}

fn check_pilgrimages(g: &Graph, p: &[Vec<usize>]) {
    let n = g.n();

    assert_eq!(p.len(), n);

    #[allow(clippy::needless_range_loop)]
    for i in 0..n {
        assert_eq!(p[i][0], i);
        g.assert_valid_pilgrimage(&p[i]);
    }
}

fn main() {
    let graph = church::gen_graph();

    print_graph(&graph);

    let Ok(warry_ans) = std::panic::catch_unwind(|| {
        let warry_ans = find_pilgrimages(&graph);
        check_pilgrimages(&graph, &warry_ans);
        warry_ans
    }) else {
        panic!("Something terrible has gone wrong. (You should report this as a bug)");
    };

    let user_ans = read_pilgrimages(&graph);

    check_pilgrimages(&graph, &user_ans);

    for (u, w) in user_ans.iter().zip(warry_ans.iter()) {
        #[allow(clippy::comparison_chain)]
        if u.len() < w.len() {
            panic!("The omniscient Warry found a better pilgrimage.");
        } else if u.len() > w.len() {
            panic!("You found a better pilgrimage than the omniscient Warry. That's impossible! (You should report this as a bug)");
        }
    }

    println!(
        "Good job. Thanks for helping Byan and proving your loyalty to the great Warry. \
         As promised, here's your flag: {}",
        include_str!("../flag.txt").trim()
    );
}
