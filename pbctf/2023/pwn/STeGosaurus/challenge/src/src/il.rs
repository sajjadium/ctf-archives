use std::cmp::max;
use std::collections::HashMap;

use serde::{Deserialize, Serialize};

#[derive(
    Serialize, Deserialize, Hash, PartialEq, Eq, PartialOrd, Ord,
    Copy, Clone, Debug
)]
pub struct LVar(pub u32);
impl std::ops::Add<u32> for LVar {
    type Output = LVar;

    fn add(self, rhs: u32) -> Self::Output {
        Self(self.0 + rhs)
    }
}

#[derive(
    Serialize, Deserialize, Hash, PartialEq, Eq, PartialOrd, Ord,
    Copy, Clone, Debug
)]
pub struct GVar(pub u32);
impl std::ops::Add<u32> for GVar {
    type Output = GVar;

    fn add(self, rhs: u32) -> Self::Output {
        Self(self.0 + rhs)
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum NumType {
    I8, U8, I16, U16, I32, U32, I64, U64,
}

impl NumType {
    #[inline]
    pub const fn signed(self) -> bool {
        use NumType::*;
        match self {
            U8 | U16 | U32 | U64 => false,
            I8 | I16 | I32 | I64 => true,
        }
    }

    #[inline]
    pub const fn mask(self) -> u64 {
        use NumType::*;
        match self {
            U8 | I8 => 0xff,
            U16 | I16 => 0xffff,
            U32 | I32 => 0xffffffff,
            U64 | I64 => 0xffffffffffffffff,
        }
    }

    #[inline]
    pub const fn bits(self) -> u64 {
        use NumType::*;
        match self {
            U8 | I8 => 8,
            U16 | I16 => 16,
            U32 | I32 => 32,
            U64 | I64 => 64,
        }
    }
}

#[derive(Clone, Copy, Debug, Serialize, Deserialize)]
pub struct Number {
    pub value: u64,
    pub tp: NumType,
}

impl Number {
    #[inline]
    pub fn op<F: Fn(u64, u64) -> u64>(self, rhs: Self, raw_op: F) -> Self {
        let tp = max(self.tp, rhs.tp);
        let value = raw_op(self.value, rhs.value) & tp.mask();
        Self { value, tp }
    }
}

#[derive(Clone, Copy, Debug, Serialize, Deserialize)]
pub enum Atom {
    Local(LVar),
    Global(GVar),
    Number(Number),
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ApplyType {
    pub name: Atom,
    pub args: Vec<Atom>,
}

#[derive(Clone, Copy, Debug, Serialize, Deserialize)]
pub enum PrimOpType {
    // Number primitive operations
    Add, Sub, Mul, Div, Rem, Shl, Shr,
    // Array primitive operations,
    New, Get, Set,
    // Generic operations
    Id, Cls,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ApplyPType {
    pub name: PrimOpType,
    pub args: Vec<Atom>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CaptureType {
    pub remap: Vec<LVar>,
    pub next: Box<STGExpr>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ConstructType {
    pub variant: Option<u64>,
    pub values: Vec<Atom>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CaseType {
    pub switch: Box<STGExpr>,
    pub alts: HashMap<Option<u64>, (STGExpr, Vec<bool>)>,
    pub default: Option<(Box<STGExpr>, bool)>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct LetType {
    pub locals: Vec<Atom>,
    pub next: Box<STGExpr>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub enum STGExpr {
    Apply(ApplyType),
    ApplyP(ApplyPType),
    Capture(CaptureType),
    Construct(ConstructType),
    Case(CaseType),
    Let(LetType),
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Closure {
    pub outer_locals: u32,
    pub args: u32,
    pub next: STGExpr,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Module {
    pub globals: HashMap<GVar, Closure>,
    pub entry: GVar,
}
