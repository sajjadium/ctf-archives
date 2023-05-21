use crate::classify::CharacterId;
use crate::pretty::{PrettyPrint, PrettyPrinter};
use std::fmt;
use std::io;
use std::io::Write;
use codemap::{Span, Spanned};

#[derive(Clone, Copy)]
pub struct Character(pub Spanned<CharacterId>);

impl fmt::Debug for Character {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.0.node.fmt(f)
    }
}

impl fmt::Display for Character {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.0.node.fmt(f)
    }
}

#[derive(Clone, Debug)]
pub struct Play {
    pub title: Span,
    pub characters: Vec<Character>,
    pub acts: Vec<Act>,
}

impl PrettyPrint for Play {
    fn print<W: Write>(&self, p: &mut PrettyPrinter<'_, W>) -> io::Result<()> {
        writeln!(p, "play:")?;
        let mut p = p.indented();
        writeln!(p, "characters: {:?}", self.characters)?;
        for act in &self.acts {
            act.print(&mut p)?;
        }
        Ok(())
    }
}

#[derive(Clone, Debug)]
pub struct Act {
    pub number: Spanned<i32>,
    pub scenes: Vec<Scene>,
}

impl PrettyPrint for Act {
    fn print<W: Write>(&self, p: &mut PrettyPrinter<'_, W>) -> io::Result<()> {
        writeln!(p, "act {}:", self.number.node)?;
        let mut p = p.indented();
        for scene in &self.scenes {
            scene.print(&mut p)?;
        }
        Ok(())
    }
}

#[derive(Clone, Debug)]
pub struct Scene {
    pub number: Spanned<i32>,
    pub events: Vec<Spanned<Event>>,
}

impl PrettyPrint for Scene {
    fn print<W: Write>(&self, p: &mut PrettyPrinter<'_, W>) -> io::Result<()> {
        writeln!(p, "scene {}:", self.number.node)?;
        let mut p = p.indented();
        for event in &self.events {
            event.print(&mut p)?;
        }
        Ok(())
    }
}

#[derive(Clone, Debug)]
pub enum Event<J = Goto> {
    Speak(Character, Vec<Spanned<Sentence<J>>>),
    Enter(Vec<Character>),
    Exit(Vec<Character>),
}

impl<J: PrettyPrint + fmt::Debug> PrettyPrint for Event<J> {
    fn print<W: Write>(&self, p: &mut PrettyPrinter<'_, W>) -> io::Result<()> {
        match self {
            Event::Speak(character, sentences) => {
                writeln!(p, "speak {:?}:", character)?;
                let mut p = p.indented();
                for sentence in sentences {
                    sentence.print(&mut p)?;
                }
            }
            Event::Enter(characters) => writeln!(p, "enter {:?}", characters)?,
            Event::Exit(characters) => writeln!(p, "exit {:?}", characters)?,
        }

        Ok(())
    }
}

#[derive(Clone, Debug)]
pub enum Sentence<J = Goto> {
    Condition(bool, Spanned<UnconditionalSentence<J>>),
    Always(UnconditionalSentence<J>),
}

impl<J: PrettyPrint + fmt::Debug> PrettyPrint for Sentence<J> {
    fn print<W: Write>(&self, p: &mut PrettyPrinter<'_, W>) -> io::Result<()> {
        match self {
            Sentence::Condition(b, then) => {
                writeln!(p, "if {:?}:", b)?;
                then.print(&mut p.indented())?;
            }
            Sentence::Always(s) => s.print(p)?,
        }

        Ok(())
    }
}

#[derive(Clone, Debug)]
pub struct Goto {
    pub direction: Spanned<GotoDirection>,
    pub target: Spanned<GotoTarget>,
}

impl PrettyPrint for Goto {
    fn print<W: Write>(&self, p: &mut PrettyPrinter<'_, W>) -> io::Result<()> {
        writeln!(p, "jump {:?} to {:?}", self.direction.node, self.target.node)
    }
}

#[derive(Clone, Debug)]
pub enum UnconditionalSentence<J = Goto> {
    Goto(J),
    Push(Spanned<Value>),
    Pop,
    InputCharacter,
    InputNumber,
    OutputCharacter,
    OutputNumber,
    Assign(Spanned<Pronoun>, Spanned<Value>),
    Question(Spanned<Value>, Spanned<Comparison>, Spanned<Value>),
}

impl<J: PrettyPrint + fmt::Debug> PrettyPrint for UnconditionalSentence<J> {
    fn print<W: Write>(&self, p: &mut PrettyPrinter<'_, W>) -> io::Result<()> {
        match self {
            UnconditionalSentence::Assign(you, value) => {
                writeln!(p, "assign {:?}:", you.node)?;
                value.print(&mut p.indented())?;
            }
            UnconditionalSentence::Question(lhs, cmp, rhs) => {
                writeln!(p, "compare {:?}:", cmp.node)?;
                let mut p = p.indented();
                lhs.print(&mut p)?;
                rhs.print(&mut p)?;
            }
            UnconditionalSentence::Goto(goto) => {
                goto.print(p)?;
            }
            UnconditionalSentence::Push(value) => {
                writeln!(p, "push:")?;
                value.print(&mut p.indented())?;
            }
            other => writeln!(p, "{:?}", other)?,
        }

        Ok(())
    }
}

#[derive(Clone, Copy, Debug)]
pub enum Pronoun {
    FirstPerson,
    SecondPerson,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum GotoDirection {
    Proceed,
    Return,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum GotoTarget {
    Act(i32),
    Scene(i32),
}

impl fmt::Display for GotoTarget {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match *self {
            GotoTarget::Act(n) => write!(f, "act {}", roman::to(n).unwrap()),
            GotoTarget::Scene(n) => write!(f, "scene {}", roman::to(n).unwrap()),
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Comparison {
    pub negated: bool,
    pub ty: ComparisonType,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum ComparisonType {
    Eq,
    Lt,
    Gt,
}

#[derive(Clone, Debug)]
pub enum Value {
    Character(Character),
    Pronoun(Spanned<Pronoun>),
    Const(i32),
    UnOp(UnOp, Box<Spanned<Value>>),
    BinOp(BinOp, Box<Spanned<Value>>, Box<Spanned<Value>>),
}

impl PrettyPrint for Value {
    fn print<W: Write>(&self, p: &mut PrettyPrinter<'_, W>) -> io::Result<()> {
        match self {
            Value::Character(character) => writeln!(p, "{:?}", character)?,
            Value::Pronoun(pronoun) => writeln!(p, "{:?}", pronoun)?,
            Value::Const(n) => writeln!(p, "const {}", n)?,
            Value::UnOp(op, arg) => {
                writeln!(p, "{op:?}:")?;
                arg.print(&mut p.indented())?;
            }
            Value::BinOp(op, lhs, rhs) => {
                writeln!(p, "{op:?}:")?;
                lhs.print(&mut p.indented())?;
                rhs.print(&mut p.indented())?;
            }
        }

        Ok(())
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum BinOp {
    Add,
    Sub,
    Mul,
    Div,
    Mod,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum UnOp {
    Twice,
    Square,
    Cube,
    Sqrt,
    Factorial,
}
