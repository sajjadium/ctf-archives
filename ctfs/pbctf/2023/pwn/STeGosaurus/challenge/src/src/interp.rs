use std::cmp::min;
use std::collections::{HashMap, BTreeMap};
use std::mem::replace;
use std::num::TryFromIntError;
use std::rc::Rc;

use crate::obj::Obj;
use crate::il;

fn iif<E>(exp: bool, true_exp: E, false_exp: E) -> E {
    if exp { true_exp } else { false_exp }
}

#[derive(Debug)]
pub enum Error {
    InvalidLocal(il::LVar),
    InvalidGlobal(il::GVar),
    /// Invalid number of arguments: expected, actual
    InvalidArgCount(usize, usize),
    InvalidFrame,
    NumberConversion,
    ExpectedArray,
    ExpectedConstruct,
    InvalidCase(Option<u64>),
    InvalidPattern(Vec<bool>, usize),
    ApplyingConstruct,
    Blackhole,
}

impl std::fmt::Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::InvalidLocal(e) => write!(f, "Invalid local #{}", e.0),
            Self::InvalidGlobal(e) => write!(f, "Invalid global #{}", e.0),
            Self::InvalidArgCount(exp, act) =>
                write!(f, "Expected {exp} arguments, but got {act} arguments"),
            Self::InvalidFrame =>
                write!(f, "Capturing closure with mismatched frames"),
            Self::NumberConversion => write!(f, "Illegal numeric conversion"),
            Self::ExpectedArray => write!(f, "Expected primitive array type"),
            Self::ExpectedConstruct => write!(f, "Expected inductive type"),
            Self::InvalidCase(cnum) => write!(f, "Unhandled case {cnum:?}"),
            Self::InvalidPattern(pat, cons_size) =>
                write!(f, "Pattern expects an {}-construct but we actually got a {cons_size}-construct", pat.len()),
            Self::ApplyingConstruct => write!(f, "Attempting to apply a construct"),
            Self::Blackhole => write!(f, "Potential infinite recursion"),
        }
    }
}
impl std::error::Error for Error {
}

impl From<TryFromIntError> for Error {
    fn from(_: TryFromIntError) -> Self {
        Self::NumberConversion
    }
}

type Res<T> = Result<T, Error>;

type HeapSlice<'l> = Obj<&'l [Obj<Value<'l>>]>;

#[derive(Clone)]
pub struct LocalMap<'l>(BTreeMap<il::LVar, HeapSlice<'l>>);
impl<'l> std::fmt::Debug for LocalMap<'l> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_tuple("LocalMap").finish()
    }
}

impl<'l> LocalMap<'l> {
    pub fn new() -> Self {
        Self(BTreeMap::new())
    }

    pub fn count(&self) -> u32 {
        self.0.last_key_value()
            .map(|(k, v)| k.0 + v.borrow().len() as u32)
            .unwrap_or(0)
    }

    pub fn get(&self, v: il::LVar) -> Option<Obj<Value<'l>>> {
        let (&start, vars) = self.0.range(..=v)
            .last()?;
        vars.borrow()
            .get(usize::try_from(v.0 - start.0)
                 .expect("u32 -> usize should be lossless"))
            .map(|v| v.clone())
    }

    pub fn trim_from(&mut self, from: il::LVar) {
        let before = self.0
            .range(..from)
            .last()
            .map(|(&start, vars)| (start, vars.clone()));
        if let Some((start, vars)) = before {
            // Check if the slice right before overlaps with our trim point
            let sz = vars.borrow().len() as u32;
            if start + sz > from {
                // Either shorten the var slice at start
                let mut slice = vars.borrow_mut();
                *slice = &slice[..from.0 as usize];
            }
        }

        // Remove any overlapping slices after our current slice
        let after: Vec<_> = self.0
            .range(from..)
            .map(|(&start, vars)| (start, vars.clone()))
            .collect();
        for (start, _) in after {
            self.0.remove(&start);
        }

    }

    pub fn append<'x>(&mut self, slice: &'x [Obj<Value<'x>>]) {
        self.0.insert(il::LVar(self.count()), obj_new!(slice, &[] as &[_]));
    }

    pub fn remap(&self, remapper: &[il::LVar]) -> Res<Self> {
        let mut ret = BTreeMap::new();
        for (i, &v) in remapper.into_iter().enumerate() {
            let (&start, vars) = self.0.range(..=v)
                .last()
                .ok_or_else(|| Error::InvalidLocal(v))?;
            let ind = usize::try_from(v.0 - start.0)
                .expect("u32 -> usize should be lossless");
            let slice = Obj::new(&vars.borrow()[ind..=ind]);
            ret.insert(il::LVar(i as u32), slice);
        }
        Ok(Self(ret))
    }
}

#[derive(Clone, Debug)]
pub struct ThunkVal<'l> {
    target: Rc<il::Closure>,
    locals: LocalMap<'l>,
}

#[derive(Clone, Debug)]
pub struct PartialApplication<'l> {
    target: Rc<il::Closure>,
    locals: LocalMap<'l>,
    args_left: u32
}

#[derive(Clone, Debug)]
pub struct Construct<'l> {
    pub variant: Option<u64>,
    pub values: Vec<Obj<Value<'l>>>,
}

#[derive(Clone, Debug)]
pub enum WeakNormalValue<'l> {
    Function(PartialApplication<'l>),
    Pap(PartialApplication<'l>),
    Construct(Construct<'l>),
    Number(il::Number),
    Array(Obj<Vec<u8>>),
    Blackhole,
}

impl WeakNormalValue<'_> {
    pub fn as_numb(&self) -> il::Number {
        match self {
            Self::Number(n) => *n,
            _ => il::Number {
                value: 0,
                tp: il::NumType::U64
            },
        }
    }
}


const BLACK_HOLE: Value<'static> = Value::Ind(WeakNormalValue::Blackhole);

#[derive(Clone, Debug)]
pub enum Value<'l> {
    Thunk(ThunkVal<'l>),
    Ind(WeakNormalValue<'l>),
}

pub struct RunState<'l> {
    entry: il::GVar,
    globals: HashMap<il::GVar, Rc<il::Closure>>,
    globals_caf: HashMap<il::GVar, Obj<Value<'l>>>,
    heap: Box<Vec<Obj<Value<'l>>>>,
}

impl<'l> RunState<'l> {
    pub fn new(entry: il::Module) -> Self {
        let globals = HashMap::from_iter(
            entry.globals
                .into_iter()
                .map(|(k, v)| (k, Rc::new(v)))
        );

        Self {
            entry: entry.entry,
            globals,
            globals_caf: HashMap::new(),
            heap: Box::new(Vec::with_capacity(100)),
        }
    }

    pub fn fetch_global(
        &mut self,
        locals: &LocalMap<'l>,
        gbl: il::GVar,
    ) -> Res<Obj<Value<'l>>> {
        // If we have already evaluated this as a CAF, return the value
        if let Some(val) = self.globals_caf.get(&gbl) {
            return Ok(val.clone());
        }

        // Fetch the global's closure value
        let closure = self.globals.get(&gbl)
            .ok_or_else(|| Error::InvalidGlobal(gbl))?
            .clone();

        // Make sure that our outer scope matches
        let locals = if locals.count() < closure.outer_locals {
            return Err(Error::InvalidFrame);
        } else {
            let mut locals = locals.clone();
            locals.trim_from(il::LVar(closure.outer_locals));
            locals
        };

        // For CAFs we should mark it as a blackhole at this point
        let val = Obj::new(Value::Ind(WeakNormalValue::Blackhole));
        if locals.count() == 0 {
            self.globals_caf.insert(gbl, val.clone());
        }

        *val.borrow_mut() = if closure.args == 0 {
            // No arguments... we have an unevaluated thunk
            Value::Thunk(ThunkVal {
                target: closure,
                locals,
            })
        } else {
            // Some number of arguments, means we have a head-normal-form value: a
            // function
            let args_left = closure.args;
            Value::Ind(WeakNormalValue::Function(PartialApplication {
                target: closure,
                locals,
                args_left,
            }))
        };

        Ok(val)
    }

    fn strict_args<const N: usize>(
        &mut self,
        args: &Vec<Obj<Value<'l>>>
    ) -> Res<[WeakNormalValue<'l>; N]> {
        if args.len() != N {
            return Err(Error::InvalidArgCount(N, args.len()));
        }

        let mut ret = [(); N].map(|_| WeakNormalValue::Blackhole);
        for i in 0..N {
            ret[i] = self.normalize(args[i].clone())?;
        }

        Ok(ret)
    }

    fn apply_prim(
        &mut self,
        op: il::PrimOpType,
        args: Vec<Obj<Value<'l>>>,
    ) -> Res<WeakNormalValue<'l>> {
        use il::PrimOpType as Op;
        use WeakNormalValue as WNV;
        Ok(WNV::Number(match op {
            Op::Add => {
                let [op1, op2] = self.strict_args(&args)?;
                op1.as_numb().op(op2.as_numb(), u64::wrapping_add)
            }
            Op::Sub => {
                let [op1, op2] = self.strict_args(&args)?;
                op1.as_numb().op(op2.as_numb(), u64::wrapping_sub)
            }
            Op::Mul => {
                let [op1, op2] = self.strict_args(&args)?;
                op1.as_numb().op(op2.as_numb(), u64::wrapping_mul)
            }
            Op::Div => {
                let [op1, op2] = self.strict_args(&args)?;
                op1.as_numb().op(op2.as_numb(), u64::wrapping_div)
            }
            Op::Rem => {
                let [op1, op2] = self.strict_args(&args)?;
                op1.as_numb().op(op2.as_numb(), u64::wrapping_rem)
            }
            Op::Shr => {
                let [op1, op2] = self.strict_args(&args)?;
                let op1 = op1.as_numb();
                let shf = op2.as_numb().value % op1.tp.bits();
                il::Number{ value: op1.value << shf, tp: op1.tp }
            }
            Op::Shl => {
                let [op1, op2] = self.strict_args(&args)?;
                let op1 = op1.as_numb();
                let shf = op2.as_numb().value % op1.tp.bits();
                let value = if op1.tp.signed() {
                    ((op1.value as i64) >> shf) as u64
                } else {
                    op1.value >> shf
                };
                il::Number{ value, tp: op1.tp }
            }
            Op::New => {
                let [op1, op2] = self.strict_args(&args)?;
                return Ok(WNV::Array(Obj::new(
                    vec![op2.as_numb().value as u8; op1.as_numb().value as usize]
                )));
            }
            Op::Set => {
                let [arr, ind, val] = self.strict_args(&args)?;
                if let WNV::Array(arr) = arr {
                    let ind = ind.as_numb();
                    let mut val = val.as_numb();
                    for i in 0..(val.tp.bits() as usize / 8) {
                        arr.borrow_mut()[ind.value as usize + i] = val.value as u8;
                        val.value >>= 8;
                    }
                    il::Number {
                        value: 0,
                        tp: il::NumType::U8,
                    }
                } else {
                    return Err(Error::ExpectedArray);
                }
            }
            Op::Get => {
                let [arr, ind, tp] = self.strict_args(&args)?;
                if let WNV::Array(arr) = arr {
                    let ind = ind.as_numb();
                    let mut value = 0;
                    let tp = tp.as_numb().tp;
                    for i in 0..(tp.bits() as usize / 8) {
                        value |= (arr.borrow_mut()[ind.value as usize + i] as u64)
                            << (i * 8);
                    }
                    il::Number {
                        value,
                        tp,
                    }
                } else {
                    return Err(Error::ExpectedArray);
                }
            }

            // For easier exploitation
            Op::Id => {
                if args.len() != 1 {
                    return Err(Error::InvalidArgCount(1, args.len()));
                }
                
                il::Number {
                    value: (&*args[0].borrow()) as *const _ as u64,
                    tp: il::NumType::U64,
                }
            }
            Op::Cls => {
                // Too lazy to write a garbage collector
                if args.len() != 1 {
                    return Err(Error::InvalidArgCount(1, args.len()));
                }

                *args[0].borrow_mut() = BLACK_HOLE;

                il::Number {
                    value: 0,
                    tp: il::NumType::U8,
                }
            }

        }))
    }

    fn apply(
        &mut self,
        nf: WeakNormalValue<'l>,
        args: Vec<Obj<Value<'l>>>,
    ) -> Res<WeakNormalValue<'l>> {
        use WeakNormalValue as NF;

        let pap = match nf {
            NF::Function(pap) => pap,
            NF::Pap(pap) => pap,
            NF::Construct(_) => return Err(Error::ApplyingConstruct),
            NF::Number(_) => return Err(Error::ApplyingConstruct),
            NF::Array(_) => return Err(Error::ApplyingConstruct),
            NF::Blackhole => return Err(Error::Blackhole),
        };

        // Insert arguments into heap
        let args_left = pap.args_left.try_into()?;
        let (applied, rest) = args.split_at(min(args.len(), args_left));
        let curpos = self.heap.len();
        for a in applied {
            self.heap.push(a.clone());
        }

        let mut locals = pap.locals.clone();
        locals.append(&self.heap[curpos..]);

        Ok(if applied.len() < args_left  {
            // Still partially application
            NF::Pap(PartialApplication {
                target: pap.target,
                locals,
                args_left: (args_left - applied.len()).try_into()?,
            })
        } else {
            // Arguments are saturated
            let ret = self.eval_expr(&pap.target.next, &locals)?;

            if rest.len() > 0 {
                // Arguments are over saturated
                self.apply(
                    ret,
                    rest.iter()
                        .map(Clone::clone)
                        .collect(),
                )?
            } else {
                ret
            }
        })
    }

    fn get_atom(
        &mut self,
        locals: &LocalMap<'l>,
        atom: &il::Atom,
    ) -> Res<Obj<Value<'l>>> {
        match atom {
            il::Atom::Local(lvar) => {
                locals
                    .get(*lvar)
                    .ok_or_else(|| Error::InvalidLocal(*lvar))
            }
            il::Atom::Global(ref gvar) => {
                self.fetch_global(&locals, *gvar)
            }
            il::Atom::Number(n) => {
                Ok(Obj::new(Value::Ind(WeakNormalValue::Number(n.clone()))))
            }
        }
    }

    fn eval_expr(&mut self, expr: &il::STGExpr, locals: &LocalMap<'l>) ->
        Res<WeakNormalValue<'l>>
    {
        match expr {
            il::STGExpr::Apply(ref ap) if ap.args.len() == 0 => {
                let atom_val = self.get_atom(locals, &ap.name)?;
                self.normalize(atom_val)
            }
            il::STGExpr::Apply(ref ap) => {
                let args = ap.args
                    .iter()
                    .map(|a| self.get_atom(&locals, a))
                    .collect::<Res<_>>()?;

                let fn_val = self.get_atom(&locals, &ap.name)?;
                let fn_nf = self.normalize(fn_val)?;
                self.apply(fn_nf, args)
            }
            il::STGExpr::Capture(ref ap) => {
                let scoped_locals = locals.remap(&ap.remap)?;
                self.eval_expr(&ap.next, &scoped_locals)
            }
            il::STGExpr::ApplyP(ref ap) => {
                let args = ap.args
                    .iter()
                    .map(|a| self.get_atom(&locals, a))
                    .collect::<Res<_>>()?;
                self.apply_prim(ap.name, args)
            }
            il::STGExpr::Let(ref lets) => {
                // Capture the needed locals
                let mut locals = locals.clone();
                let heap_top = self.heap.len();
                let locals_cnt = locals.count();
                for local_val in &lets.locals {
                    let val = self.get_atom(&locals, local_val)?;
                    self.heap.push(val);
                    locals.trim_from(il::LVar(locals_cnt));
                    locals.append(&self.heap[heap_top..]);
                }

                self.eval_expr(&*lets.next, &locals)
            }
            il::STGExpr::Construct(ref cnst) => {
                Ok(WeakNormalValue::Construct(Construct {
                    variant: cnst.variant,
                    values: cnst.values
                        .iter()
                        .map(|a| self.get_atom(locals, a))
                        .collect::<Res<_>>()?,
                }))
            }
            il::STGExpr::Case(ref case) => {
                enum Pat<'c> {
                    None,
                    Itself,
                    Destruct(&'c [bool]),
                }
                let res = self.eval_expr(&case.switch, locals)?;
                if let WeakNormalValue::Construct(cnst) = &res {
                    // Select the correct case expresion based on variant
                    // in construction
                    let (case_expr, bindings) = case.alts.get(&cnst.variant)
                        .map(|(ref e, ref pat)| {
                            (e, Pat::Destruct(pat.as_ref()))
                        })
                        .or(case.default.as_ref().map(|(e, pat)| {
                            (&**e, iif(*pat, Pat::Itself, Pat::None))
                        }))
                        .ok_or_else(|| Error::InvalidCase(cnst.variant.clone()))?;

                    // Add any necessary bindings to heap
                    let heap_top = self.heap.len();
                    match bindings {
                        Pat::None => {},
                        Pat::Itself => {
                            self.heap.push(Obj::new(Value::Ind(res.clone())));
                        }
                        Pat::Destruct(pat) => {
                            if pat.len() != cnst.values.len() {
                                return Err(Error::InvalidPattern(
                                    pat.to_vec(),
                                    cnst.values.len(),
                                ));
                            }

                            for (&p, val) in pat.iter().zip(cnst.values.iter()) {
                                if p { self.heap.push(val.clone()) }
                            }
                        }
                    }

                    // Check if we touched our heap, if so, we should change our
                    // locals scope to add those into the scope
                    if heap_top == self.heap.len() {
                        self.eval_expr(case_expr, locals)
                    } else {
                        let mut locals = locals.clone();
                        locals.append(&self.heap[heap_top..]);
                        self.eval_expr(case_expr, &locals)
                    }
                } else {
                    if case.alts.len() != 0 {
                        Err(Error::ExpectedConstruct)
                    } else if let Some((case_expr, bindings)) = &case.default {
                        if *bindings {
                            self.heap.push(Obj::new(Value::Ind(res.clone())));

                            let mut locals = locals.clone();
                            locals.append(&self.heap[self.heap.len() - 1..]);
                            self.eval_expr(case_expr, &locals)
                        } else {
                            self.eval_expr(case_expr, locals)
                        }
                    } else {
                        Err(Error::InvalidCase(None))
                    }
                }
            }
         }
    }

    pub fn normalize(
        &mut self,
        val_ref: Obj<Value<'l>>,
    ) -> Res<WeakNormalValue<'l>> {
        use Value as V;
        let val = replace(&mut *val_ref.borrow_mut(), BLACK_HOLE);
        let nf = match val {
            V::Thunk(thk) => self.eval_expr(&thk.target.next, &thk.locals)?,
            V::Ind(nf) => nf,
        };
        *val_ref.borrow_mut() = Value::Ind(nf.clone());
        Ok(nf)
    }

    fn destruct<const N: usize>(
        &mut self,
        variant: Option<u64>,
        val: WeakNormalValue<'l>,
    ) -> Res<[Obj<Value<'l>>; N]> {
        match val {
            WeakNormalValue::Construct(val) => {
                if variant != val.variant {
                    return Err(Error::InvalidCase(val.variant));
                }
                match val.values.as_chunks() {
                    ([chk], []) => Ok(chk.clone()),
                    _ => {
                        Err(Error::InvalidPattern(
                            vec![true; N],
                            val.values.len(),
                        ))
                    }
                }
            }
            _ => {
                return Err(Error::ExpectedConstruct);
            }
        }
    }

    pub fn entrypoint(&mut self) -> Res<()> {
        let lm = LocalMap::new();
        let gbl = self.fetch_global(&lm, self.entry)?;
        let tok = Obj::new(Value::Ind(WeakNormalValue::Construct(Construct {
            variant: None,
            values: Vec::new(),
        })));
        let gbl = self.normalize(gbl)?;
        let [io] = self.destruct(None, gbl)?;
        let io = self.normalize(io)?;
        let io_res = self.apply(io, vec![tok])?;
        let [_tok, ret] = self.destruct(None, io_res)?;
        let _ret = self.normalize(ret)?;

        Ok(())
    }
}
