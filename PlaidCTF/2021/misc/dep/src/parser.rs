use crate::Term;
use crate::Term_::{self, *};

use std::str::FromStr;

use nom::{complete, do_parse, eat_separator, map_res, named, opt, sep, tag, take_while1};

named!(space(&str)->&str, eat_separator!(" \t\n"));

fn is_identifier_char(x: char) -> bool {
    x.is_alphanumeric() || x == '_'
}

fn is_digit(x: char) -> bool {
    match x {
        '0'..='9' => true,
        _ => false,
    }
}

named!(
    identifier(&str)->String,
    do_parse!(
        x: take_while1!(is_identifier_char) >> (x.into())
    )
);

named!(
    parse_u8(&str)->u8,
    map_res!(take_while1!(is_digit), |x| {
        u8::from_str(x)
    })
);

named!(
    assignment(&str)->Option<String>,
    opt!(complete!(sep!(space, terminated!(identifier, tag!("=")))))
);

named!(variable(&str)->Term_, do_parse!(x: identifier >> (Variable(x))));

named!(
    sort(&str)->Term_,
    do_parse!(tag!("#") >> n: parse_u8 >> (Sort(n)))
);

named!(
    application(&str)->Term_,
    sep!(
        space,
        do_parse!(
            tag!("(") >> f: term >> xs: many1!(term)
                >> tag!(")") >> ({
                    let mut res = f;
                    for x in xs {
                        res = Application(res.into(), x.into());
                    }
                    res
                })
        )
    )
);

named!(
    abstraction_or_pi(&str)->Term_,
    sep!(
        space,
        do_parse!(
            x_t: delimited!(
                tag!("("),
                do_parse!(x: identifier >> tag!(":") >> t: term >> (x, t)),
                tag!(")")
            ) >> typ: alt!(tag!("->") | tag!("=>"))
                >> e: term
                >> ({
                    let (x, t) = x_t;
                    match typ {
                        "->" => Abstraction(x.into(), t.into(), e.into()),
                        "=>" => Pi(x.into(), t.into(), e.into()),
                        _ => unreachable!(),
                    }
                })
        )
    )
);

named!(
    term(&str)->Term_,
    sep!(
        space,
        
        alt!(
            delimited!(tag!("("), term, tag!(")")) |         
            sort | abstraction_or_pi | variable | application
        )
    )
);

named!(
    pub parse(&str)->(Option<String>, Term),
    do_parse!(
        a: assignment >>
        t: term >>
        (a, t.into())
    )
);

pub fn parse_many(s: &str) -> (&str, Vec<(String, Option<String>, Term)>, crate::Err<()>) {
    let mut res = vec![];
    let mut s = s;
    loop {
        match parse(s) {
            Ok((rem, (name, term))) => {
                let used = String::from(s[0..s.len() - rem.len()].trim_start());
                s = rem;
                res.push((used, name, term));
            }
            Err(nom::Err::Incomplete(_)) => {
                return (s, res, Ok(()));
            }
            Err(e) => {
                return (&s[s.len()..], res, Err(e.to_string()));
            }
        }
    }
}
