use std::collections::HashSet;

use proc_macro2::Span;
use stegosaurus::il;
use syn::{parse::Parse, punctuated::Punctuated};

trait Lookahead {
    fn lookahead(la: &syn::parse::Lookahead1) -> bool;
}

pub struct CAF {
    #[allow(dead_code)]
    fn_tok: syn::Token!(fn),
    pub name: syn::Ident,
    #[allow(dead_code)]
    paren_tok: Option<syn::token::Paren>,
    pub args: Punctuated<Var, syn::Token!(,)>,
    #[allow(dead_code)]
    brace_tok: syn::token::Brace,
    pub expr: Expr,
}

impl Parse for CAF {
    fn parse(input: syn::parse::ParseStream) -> syn::Result<Self> {
        let args;
        let body;

        Ok(Self {
            fn_tok: input.parse()?,
            name: input.parse()?,
            paren_tok: if input.peek(syn::token::Paren){
                let args_toks;
                let ret = syn::parenthesized!(args_toks in input);
                args = args_toks.parse_terminated(Parse::parse)?;
                Some(ret)
            } else {
                args = Punctuated::new();
                None
            },
            args,
            brace_tok: syn::braced!(body in input),
            expr: body.parse()?,
        })

    }
}

pub enum Var {
    Wildcard(syn::Token!(_)),
    Var(syn::Ident),
}

impl Lookahead for Var {
    fn lookahead(la: &syn::parse::Lookahead1) -> bool {
        la.peek(syn::Token!(_)) || la.peek(syn::Ident)
    }
}

impl Parse for Var {
    fn parse(input: syn::parse::ParseStream) -> syn::Result<Self> {
        let la = input.lookahead1();
        if la.peek(syn::Token!(_)) {
            Ok(Var::Wildcard(input.parse()?))
        } else if la.peek(syn::Ident) {
            Ok(Var::Var(input.parse()?))
        } else {
            Err(la.error())
        }
    }
}

impl Var {
    fn scope_freevars(&self, freevars: &mut HashSet<syn::Ident>) {
        match self {
            Self::Wildcard(_) => true,
            Self::Var(v) => freevars.remove(v),
        };
    }

    pub fn span(&self) -> Span {
        match self {
            Self::Wildcard(v) => v.span,
            Self::Var(v) => v.span(),
        }
    }
}

pub enum Expr {
    Apply(ApplyType),
    Construct(ConstructType),
    Case(CaseType),
    Let(LetType),
    Do(DoType),
}

impl Expr {
    pub fn freevars(&self) -> HashSet<syn::Ident> {
        match self {
            Self::Apply(exp) => {
                let mut ret = exp.name.freevars();
                for arg in &exp.args {
                    ret.extend(arg.freevars());
                }
                ret
            },
            Self::Construct(exp) => {
                let mut ret = HashSet::new();
                for arg in &exp.values {
                    ret.extend(arg.freevars());
                }
                ret
            },
            Self::Case(exp) => {
                let mut ret = exp.expr.freevars();
                for arm in &exp.alts {
                    let mut fv = arm.expr.freevars();
                    match &arm.pattern {
                        Pattern::Binding(patt) => patt.scope_freevars(&mut fv),
                        Pattern::Construct(patt) => {
                            for val in &patt.values {
                                val.scope_freevars(&mut fv);
                            }
                        }
                    }
                    ret.extend(fv);
                }
                ret
            }
            Self::Let(exp) => {
                let mut ret = exp.next.freevars();
                for item in exp.items.iter().rev() {
                    item.binding.scope_freevars(&mut ret);
                    let mut fv = item.value.freevars();
                    for arg in &item.args {
                        arg.scope_freevars(&mut fv);
                    }
                    ret.extend(fv);
                }
                ret
            }
            Self::Do(exp) => {
                let mut ret = HashSet::new();
                for action in &exp.actions {
                    ret.extend(action.freevars());
                }
                ret
            }
        }
    }
}

impl Lookahead for Expr {
    fn lookahead(la: &syn::parse::Lookahead1) -> bool {
        ApplyType::lookahead(la) ||
        ConstructType::lookahead(la) ||
        CaseType::lookahead(la) ||
        LetType::lookahead(la) ||
        DoType::lookahead(la)
    }
}

impl Parse for Expr {
    fn parse(input: syn::parse::ParseStream) -> syn::Result<Self> {
        let la = input.lookahead1();
        Ok(if ApplyType::lookahead(&la) {
            Self::Apply(input.parse()?)
        } else if ConstructType::lookahead(&la) {
            Self::Construct(input.parse()?)
        } else if CaseType::lookahead(&la) {
            Self::Case(input.parse()?)
        } else if LetType::lookahead(&la) {
            Self::Let(input.parse()?)
        } else if DoType::lookahead(&la) {
            Self::Do(input.parse()?)
        } else {
            return Err(la.error());
        })
    }
}

pub struct ApplyType {
    pub name: AtomOrPrim,
    #[allow(dead_code)]
    paren_tok: Option<syn::token::Paren>,
    pub args: Punctuated<Atom, syn::Token!(,)>,
}

impl Lookahead for ApplyType {
    fn lookahead(la: &syn::parse::Lookahead1) -> bool {
        AtomOrPrim::lookahead(la)
    }
}

pub enum AtomOrPrim {
    Atom(Atom),
    PrimOp(syn::Token!(#), il::PrimOpType),
}

impl Lookahead for AtomOrPrim {
    fn lookahead(la: &syn::parse::Lookahead1) -> bool {
        la.peek(syn::Token!(#)) || Atom::lookahead(la)
    }
}

impl Parse for AtomOrPrim {
    fn parse(input: syn::parse::ParseStream) -> syn::Result<Self> {
        use il::PrimOpType as OP;
        let la = input.lookahead1();
        if Atom::lookahead(&la) {
            Ok(AtomOrPrim::Atom(input.parse()?))
        } else if la.peek(syn::Token!(#)) {
            let tok = input.parse()?;
            let name: syn::Ident = input.parse()?;
            let pop = match name.to_string().as_str() {
                "id"  => OP::Id,
                "cls" => OP::Cls,
                "add" => OP::Add,
                "sub" => OP::Sub,
                "mul" => OP::Mul,
                "div" => OP::Div,
                "rem" => OP::Rem,
                "shl" => OP::Shl,
                "shr" => OP::Shr,
                "new" => OP::New,
                "get" => OP::Get,
                "set" => OP::Set,
                _ => return Err(syn::Error::new(
                    name.span(),
                    "invalid primitive operator"
                )),
            };
            Ok(AtomOrPrim::PrimOp(tok, pop))
        } else {
            Err(la.error())
        }
    }
}


impl AtomOrPrim {
    fn freevars(&self) -> HashSet<syn::Ident> {
        match self {
            Self::Atom(val) => val.freevars(),
            Self::PrimOp(_, _) => HashSet::new(),
        }
    }
}

impl Parse for ApplyType {
    fn parse(input: syn::parse::ParseStream) -> syn::Result<Self> {
        let args;
        Ok(Self {
            name: input.parse()?,
            paren_tok: if input.peek(syn::token::Paren){
                let args_toks;
                let ret = syn::parenthesized!(args_toks in input);
                args = args_toks.parse_terminated(Parse::parse)?;
                Some(ret)
            } else {
                args = Punctuated::new();
                None
            },
            args,
        })
    }
}

pub struct ConstructType {
    #[allow(dead_code)]
    brace_tok: syn::token::Brace,
    pub variant: Option<syn::LitInt>,
    #[allow(dead_code)]
    pipeline_tok: Option<syn::Token!(|)>,
    pub values: Punctuated<Atom, syn::Token!(,)>,
}

impl Lookahead for ConstructType {
    fn lookahead(la: &syn::parse::Lookahead1) -> bool {
        la.peek(syn::token::Brace)
    }
}

impl Parse for ConstructType {
    fn parse(input: syn::parse::ParseStream) -> syn::Result<Self> {
        let body;
        Ok(Self {
            brace_tok: syn::braced!(body in input),
            variant: body.parse()?,
            pipeline_tok: body.parse()?,
            values: body.parse_terminated(Parse::parse)?,
        })
    }
}

pub struct CaseType {
    #[allow(dead_code)]
    match_tok: syn::Token!(match),
    pub expr: Box<Expr>,
    #[allow(dead_code)]
    brace_tok: syn::token::Brace,
    pub alts: Punctuated<MatchArm, syn::Token!(,)>,
}

impl Lookahead for CaseType {
    fn lookahead(la: &syn::parse::Lookahead1) -> bool {
        la.peek(syn::Token!(match))
    }
}

impl Parse for CaseType {
    fn parse(input: syn::parse::ParseStream) -> syn::Result<Self> {
        let body;
        Ok(Self {
            match_tok: input.parse()?,
            expr: input.parse()?,
            brace_tok: syn::braced!(body in input),
            alts: body.parse_terminated(Parse::parse)?,
        })
    }
}

pub struct MatchArm {
    pub pattern: Pattern,
    #[allow(dead_code)]
    arrow_tok: syn::Token!(=>),
    pub expr: Box<Expr>,
}

impl Lookahead for MatchArm {
    fn lookahead(la: &syn::parse::Lookahead1) -> bool {
        Pattern::lookahead(la)
    }
}

impl Parse for MatchArm {
    fn parse(input: syn::parse::ParseStream) -> syn::Result<Self> {
        Ok(Self {
            pattern: input.parse()?,
            arrow_tok: input.parse()?,
            expr: input.parse()?,
        })
    }
}

pub enum Pattern {
    Construct(PatternConstruct),
    Binding(Var),
}

impl Lookahead for Pattern {
    fn lookahead(la: &syn::parse::Lookahead1) -> bool {
        PatternConstruct::lookahead(la) || Var::lookahead(la)
    }
}

impl Parse for Pattern {
    fn parse(input: syn::parse::ParseStream) -> syn::Result<Self> {
        let la = input.lookahead1();
        Ok(if PatternConstruct::lookahead(&la) {
            Self::Construct(input.parse()?)
        } else if Var::lookahead(&la) {
            Self::Binding(input.parse()?)
        } else {
            return Err(la.error());
        })
    }
}

pub struct PatternConstruct {
    brace_tok: syn::token::Brace,
    pub variant: Option<syn::LitInt>,
    #[allow(dead_code)]
    pipeline_tok: Option<syn::Token!(|)>,
    pub values: Punctuated<Var, syn::Token!(,)>,
}

impl Lookahead for PatternConstruct {
    fn lookahead(la: &syn::parse::Lookahead1) -> bool {
        la.peek(syn::token::Brace)
    }
}

impl Parse for PatternConstruct {
    fn parse(input: syn::parse::ParseStream) -> syn::Result<Self> {
        let body;
        Ok(Self {
            brace_tok: syn::braced!(body in input),
            variant: body.parse()?,
            pipeline_tok: body.parse()?,
            values: body.parse_terminated(Parse::parse)?,
        })
    }
}

impl PatternConstruct {
    pub fn span(&self) -> Span {
        self.brace_tok.span
    }
}

pub struct LetType {
    #[allow(dead_code)]
    let_tok: syn::Token!(let),
    #[allow(dead_code)]
    brace_tok: syn::token::Brace,
    pub items: Punctuated<LetItem, syn::Token!(,)>,
    #[allow(dead_code)]
    in_tok: syn::Token!(in),
    pub next: Box<Expr>,
}

impl Lookahead for LetType {
    fn lookahead(la: &syn::parse::Lookahead1) -> bool {
        la.peek(syn::Token!(let))
    }
}

impl Parse for LetType {
    fn parse(input: syn::parse::ParseStream) -> syn::Result<Self> {
        let decls;
        Ok(Self {
            let_tok: input.parse()?,
            brace_tok: syn::braced!(decls in input),
            items: decls.parse_terminated(Parse::parse)?,
            in_tok: input.parse()?,
            next: input.parse()?,
        })
    }
}

pub struct LetItem {
    pub binding: Var,
    #[allow(dead_code)]
    paren_tok: Option<syn::token::Paren>,
    pub args: Punctuated<Var, syn::Token!(,)>,
    #[allow(dead_code)]
    pub eq_tok: syn::Token!(=),
    pub value: Box<Expr>,
}

impl Lookahead for LetItem {
    fn lookahead(la: &syn::parse::Lookahead1) -> bool {
        Var::lookahead(la)
    }
}

impl Parse for LetItem {
    fn parse(input: syn::parse::ParseStream) -> syn::Result<Self> {
        let args;
        Ok(Self {
            binding: input.parse()?,
            paren_tok: if input.peek(syn::token::Paren){
                let args_toks;
                let ret = syn::parenthesized!(args_toks in input);
                args = args_toks.parse_terminated(Parse::parse)?;
                Some(ret)
            } else {
                args = Punctuated::new();
                None
            },
            args,
            eq_tok: input.parse()?,
            value: input.parse()?,
        })
    }
}

pub struct DoType {
    pub do_tok: syn::Token!(do),
    #[allow(dead_code)]
    brace_tok: syn::token::Brace,
    pub actions: Punctuated<Expr, syn::Token!(,)>,
}

impl Lookahead for DoType {
    fn lookahead(la: &syn::parse::Lookahead1) -> bool {
        la.peek(syn::Token!(do))
    }
}

impl Parse for DoType {
    fn parse(input: syn::parse::ParseStream) -> syn::Result<Self> {
        let body;
        Ok(Self {
            do_tok: input.parse()?,
            brace_tok: syn::braced!(body in input),
            actions: body.parse_terminated(Parse::parse)?,
        })
    }
}

pub enum Atom {
    Var(syn::Ident),
    Integer(syn::LitInt),
}

impl Lookahead for Atom {
    fn lookahead(la: &syn::parse::Lookahead1) -> bool {
        la.peek(syn::LitInt) || la.peek(syn::Ident)
    }
}

impl Parse for Atom {
    fn parse(input: syn::parse::ParseStream) -> syn::Result<Self> {
        let la = input.lookahead1();
        if la.peek(syn::Ident) {
            Ok(Atom::Var(input.parse()?))
        } else if la.peek(syn::LitInt) {
            Ok(Atom::Integer(input.parse()?))
        } else {
            Err(la.error())
        }
    }
}

impl Atom {
    fn freevars(&self) -> HashSet<syn::Ident> {
        match self {
            Self::Var(atom) => HashSet::from_iter(vec![atom.clone()]),
            Self::Integer(_) => HashSet::new(),
        }
    }

    pub fn span(&self) -> Span {
        match self {
            Self::Var(atom) => atom.span(),
            Self::Integer(atom) => atom.span(),
        }
    }
}
