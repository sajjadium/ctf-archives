use std::{
    collections::HashMap,
    cell::{RefCell, Cell},
    rc::{Rc, Weak}
};

use proc_macro2::{Ident, Span};
use syn::{punctuated::Punctuated, parse::Parse};

use stegosaurus::il;
use crate::ast;


enum VarInd {
    Global(il::GVar, Span), Local(il::LVar, Span),
}

struct Scope {
    weak: Weak<Scope>,
    parent: Option<Rc<Scope>>,
    root: Rc<RefCell<Root>>,
    symtab: RefCell<HashMap<syn::Ident, il::LVar>>,
    next_local: Cell<il::LVar>,
}

impl Scope {
    fn new(root: Rc<RefCell<Root>>) -> Rc<Self> {
        Rc::new_cyclic(|weak| {
            let weak = weak.clone();
            Self {
                weak,
                parent: None,
                root,
                symtab: RefCell::new(HashMap::new()),
                next_local: Cell::new(il::LVar(0)),
            }
        })
    }

    fn push_scope(&self) -> Rc<Self> {
        Rc::new_cyclic(|weak| {
            let weak = weak.clone();
            let parent = Some(self.weak
                .upgrade()
                .expect("self pointer should still exist"));
            Self {
                weak,
                parent,
                root: self.root.clone(),
                symtab: RefCell::new(HashMap::new()),
                next_local: Cell::new(self.next_local.get()),
            }
        })
    }

    fn decl_local(&self, name: syn::Ident) {
        let ind = self.next_local.get();
        self.next_local.set(ind + 1);
        self.symtab.borrow_mut().insert(name, ind);
    }

    fn decl_local_var(&self, name: &ast::Var) {
        let ind = self.next_local.get();
        self.next_local.set(ind + 1);
        match name {
            ast::Var::Var(v) => self.symtab.borrow_mut().insert(v.clone(), ind),
            ast::Var::Wildcard(_) => None,
        };
    }

    fn decl_local_anony(&self) -> il::LVar {
        let ind = self.next_local.get();
        self.next_local.set(ind + 1);
        ind
    }

    fn var(&self, name: &syn::Ident) -> syn::Result<VarInd> {
        if let Some(var) = self.symtab.borrow().get(name) {
            return Ok(VarInd::Local(*var, name.span()))
        }

        match &self.parent {
            Some(parent) => parent.var(name),
            None => {
                self.root
                    .borrow()
                    .global_symtab
                    .get(name)
                    .map(|v| VarInd::Global(*v, name.span()))
                    .ok_or_else(|| syn::Error::new(name.span(), "Unknown identifier"))
            }
        }
    }

    fn decl_global(&self, name: syn::Ident) -> il::GVar {
        self.init_global(Some(name), il::Closure {
            outer_locals: 0,
            args: 0,
            next: il::STGExpr::Construct(il::ConstructType {
                variant: None,
                values: Vec::new(),
            }),
        })
    }

    fn init_global(&self, name: Option<syn::Ident>, closure: il::Closure) -> il::GVar {
        let mut root = self.root.borrow_mut();
        let var = il::GVar(root.globals.len() as u32);
        if let Some(name) = name {
            if let Some(&var) = root.global_symtab.get(&name) {
                root.globals[var.0 as usize] = closure;
                return var;
            }
            root.global_symtab.insert(name, var);
        }

        root.globals.push(closure);
        var
    }
}

#[derive(Default)]
struct Root {
    globals: Vec<il::Closure>,
    global_symtab: HashMap<syn::Ident, il::GVar>,
}

trait Compile {
    type Target;
    fn compile(&self, scope: &Scope) -> syn::Result<Self::Target>;
}

impl Compile for VarInd {
    type Target = il::Atom;

    fn compile(&self, scope: &Scope) -> syn::Result<Self::Target> {
        Ok(match self {
            Self::Global(var, span) => {
                // We want to ensure that this specific usage of a global
                // variable corresponds with the number of variables we would
                // expect in the closure of said global code
                let scope_vars = scope.root
                    .borrow()
                    .globals[var.0 as usize]
                    .outer_locals;
                if scope_vars != 0 {
                    return Err(syn::Error::new(
                        *span,
                        format!("Expected {scope_vars} variables in closure but got 0."),
                    ));
                }
                il::Atom::Global(*var)
            }
            Self::Local(var, _) => il::Atom::Local(*var),
        })
    }

}

impl<T: Compile, P> Compile for Punctuated<T, P> {
    type Target = Vec<T::Target>;

    fn compile(&self, scope: &Scope) -> syn::Result<Self::Target> {
        self.iter()
            .map(|t| t.compile(scope))
            .collect()
    }
}

impl Compile for ast::Atom {
    type Target = il::Atom;

    fn compile(&self, scope: &Scope) -> syn::Result<Self::Target> {
        Ok(match self {
            Self::Var(atom) => scope.var(atom)?
                .compile(scope)?,
            Self::Integer(atom) => {
                let value = if atom.to_string().starts_with("-") {
                    atom.base10_parse::<i64>()? as u64
                } else {
                    atom.base10_parse()?
                };

                let tp = match atom.suffix() {
                    "u8"  => il::NumType::U8,
                    "u16" => il::NumType::U16,
                    "u32" => il::NumType::U32,
                    "u64" => il::NumType::U64,
                    "i8"  => il::NumType::I8,
                    "i16" => il::NumType::I16,
                    "i32" => il::NumType::I32,
                    "i64" => il::NumType::I64,
                    "" => il::NumType::I32,
                    _ => return Err(syn::Error::new(atom.span(), "Invalid suffix")),
                };

                il::Atom::Number(il::Number { value, tp })
            }
        })
    }
}

impl Compile for ast::Var {
    type Target = il::LVar;

    fn compile(&self, scope: &Scope) -> syn::Result<Self::Target> {
        Ok(match self {
            Self::Var(v) => {
                match scope.var(v)? {
                    VarInd::Local(v, _) => v,
                    VarInd::Global(_, _) => {
                        return Err(syn::Error::new(
                            v.span(),
                            "Expected local variable"
                        ));
                    }
                }
            }
            Self::Wildcard(_) => il::LVar(0),
        })
    }
}

impl Compile for ast::Expr {
    type Target = il::STGExpr;

    fn compile(&self, scope: &Scope) -> syn::Result<Self::Target> {
        Ok(match self {
            Self::Apply(exp) => {
                match &exp.name {
                    ast::AtomOrPrim::Atom(name) => il::STGExpr::Apply(il::ApplyType {
                        name: name.compile(scope)?,
                        args: exp.args.compile(scope)?,
                    }),
                    &ast::AtomOrPrim::PrimOp(_, name) => il::STGExpr::ApplyP(il::ApplyPType {
                        name,
                        args: exp.args.compile(scope)?,
                    })
                }
            }
            Self::Construct(exp) => il::STGExpr::Construct(il::ConstructType {
                variant: match &exp.variant {
                    Some(v) => Some(v.base10_parse()?),
                    None => None
                },
                values: exp.values.compile(scope)?,
            }),
            Self::Case(exp) => {
                let mut alts = HashMap::new();
                let mut default = None;
                for arm in &exp.alts {
                    let new_scope = scope.push_scope();
                    match &arm.pattern {
                        ast::Pattern::Binding(patt) => {
                            if default.is_some() {
                                return Err(syn::Error::new(
                                    patt.span(),
                                    "Unused arm",
                                ));
                            }

                            let has_binding = if let ast::Var::Var(v) = patt {
                                new_scope.decl_local(v.clone());
                                true
                            } else {
                                false
                            };

                            default = Some((
                                Box::new(arm.expr.compile(&new_scope)?),
                                has_binding,
                            ));
                        }

                        ast::Pattern::Construct(patt) => {
                            let variant = match &patt.variant {
                                Some(v) => Some(v.base10_parse()?),
                                None => None
                            };

                            if alts.contains_key(&variant) {
                                return Err(syn::Error::new(
                                    patt.span(),
                                    "Unused arm",
                                ));
                            }

                            let mut bindings = Vec::new();
                            for v in &patt.values {
                                bindings.push(if let ast::Var::Var(v) = v {
                                    new_scope.decl_local(v.clone());
                                    true
                                } else {
                                    false
                                });
                            }

                            alts.insert(variant, (
                                arm.expr.compile(&new_scope)?,
                                bindings,
                            ));
                        }
                    }
                }

                il::STGExpr::Case(il::CaseType {
                    switch: Box::new(exp.expr.compile(scope)?),
                    alts,
                    default,
                })
            },

            Self::Let(exp) => {
                il::STGExpr::Let(il::LetType {
                    locals: {
                        let mut ret = Vec::new();
                        for item in &exp.items {
                            let scope_inner = scope.push_scope();
                            for arg in &item.args {
                                scope_inner.decl_local_var(arg);
                            }

                            let next = item.value.compile(&scope_inner)?;
                            ret.push(match &next {
                                il::STGExpr::Apply(value) => {
                                    if value.args.is_empty() {
                                        Some(value.name)
                                    } else {
                                        None
                                    }
                                }
                                _ => None,
                            }.unwrap_or_else(|| {
                                let args = item.args
                                        .len()
                                        .try_into()
                                        .expect("args size should be small enough");
                                let closure = il::Closure {
                                    outer_locals: scope.next_local.get().0,
                                    args,
                                    next,
                                };

                                il::Atom::Global(scope.init_global(None, closure))
                            }));

                            scope.decl_local_var(&item.binding);
                        }
                        ret
                    },
                    next: Box::new(exp.next.compile(&scope.push_scope())?),
                })
            }

            Self::Do(exp) => {
                let mut ret = None;
                for action in exp.actions.iter().rev() {
                    ret = Some(il::STGExpr::Case(il::CaseType {
                        switch: Box::new(action.compile(&scope.push_scope())?),
                        alts: HashMap::new(),
                        default: Some(match ret {
                            Some(exp) => (Box::new(exp), false),
                            None => {
                                let scope = scope.push_scope();
                                (
                                    Box::new(il::STGExpr::Apply(il::ApplyType {
                                        name: il::Atom::Local(scope.decl_local_anony()),
                                        args: Vec::new(),
                                    })),
                                    true,
                                )
                            }
                        }),
                    }));
                }

                match ret {
                    None => return Err(syn::Error::new(exp.do_tok.span, "Empty do block")),
                    Some(ret) => ret
                }
            }
        })
    }
}

impl Compile for ast::CAF {
    type Target = il::Closure;

    fn compile(&self, scope: &Scope) -> syn::Result<Self::Target> {
        for arg in &self.args {
            scope.decl_local_var(arg);
        }

        Ok(il::Closure {
            outer_locals: 0,
            args: self.args
                .len()
                .try_into()
                .expect("args size should be small enough"),
            next: self.expr.compile(&scope)?,
        })
    }
}

pub struct Module(pub Vec<ast::CAF>);

impl Parse for Module {
    fn parse(input: syn::parse::ParseStream) -> syn::Result<Self> {
        let mut ret = Vec::new();
        while !input.is_empty() {
            ret.push(input.parse()?);
        }
        Ok(Self(ret))
    }
}

impl Module {
    pub fn compile(&self) -> syn::Result<il::Module> {
        let scope = Scope::new(Default::default());
        let root = scope.root.clone();
        for caf in &self.0 {
            if scope.var(&caf.name).is_ok() {
                return Err(syn::Error::new(caf.name.span(), "Duplicate definitions"));
            }
            scope.decl_global(caf.name.clone());
        }

        let default = Span::call_site();
        let entry = scope.var(&Ident::new("main", default))
            .map_err(|_| syn::Error::new(
                default,
                "Unable to find main() function",
            ))
            .map(|v| match v {
                VarInd::Local(_, _) => panic!("should not have local vars now"),
                VarInd::Global(gvar, _) => gvar,
            })?;

        for caf in &self.0 {
            scope.init_global(
                Some(caf.name.clone()),
                caf.compile(&scope.push_scope())?,
            );
        }

        let mut globals = HashMap::new();
        for (i, global) in root.borrow().globals.iter().enumerate() {
            globals.insert(
                il::GVar(i.try_into().expect("index should be small")),
                global.clone(),
            );
        }

        Ok(il::Module { globals, entry })
    }
}
