use crate::ast::{Character, UnOp, BinOp, ComparisonType};
use crate::pretty::PrettyPrinter;
use crate::resolve::{Block, BlockId, Condition, EndAction, Expr, Instruction};
use std::io;
use std::io::Write;

pub fn emit(blocks: &[Block], characters: &[Character], mut output: impl Write) -> io::Result<()> {
    let mut out = PrettyPrinter::new(&mut output);

    writeln!(out, "{}", include_str!("rattlespike.h"))?;
    writeln!(out)?;
    writeln!(out, "int main() {{")?;

    let mut body = out.indented();
    writeln!(body, "bool flag;")?;
    for character in characters {
        writeln!(body, "struct character {} = {{0,}};", character.0.varname())?;
    }
    writeln!(body)?;
    writeln!(body, "setvbuf(stdout, NULL, _IONBF, 0);")?;

    for (i, block) in blocks.iter().enumerate() {
        writeln!(body, "bb{i}:")?;
        emit_block(block, &mut body)?;
        writeln!(body)?;
    }

    writeln!(out, "}}")?;

    Ok(())
}

fn emit_block(block: &Block, out: &mut PrettyPrinter<'_, impl Write>) -> io::Result<()> {
    for (condition, instruction) in &block.instructions {
        match condition {
            Condition::Always => emit_instruction(instruction, out)?,
            Condition::IfTrue => {
                writeln!(out, "if (flag) {{")?;
                emit_instruction(instruction, &mut out.indented())?;
                writeln!(out, "}}")?;
            }
            Condition::IfFalse => {
                writeln!(out, "if (!flag) {{")?;
                emit_instruction(instruction, &mut out.indented())?;
                writeln!(out, "}}")?;
            }
        }
    }

    match block.next {
        EndAction::Goto(BlockId(block)) => writeln!(out, "goto bb{block};")?,
        EndAction::ExitProgram => writeln!(out, "return 0;")?,
        EndAction::Unreachable => {}
    }

    Ok(())
}

fn emit_instruction(instruction: &Instruction, out: &mut PrettyPrinter<'_, impl Write>) -> io::Result<()> {
    match instruction {
        Instruction::Assign(ch, expr) => {
            write!(out, "{}.value = ", ch.varname())?;
            emit_expr(expr, out)?;
            writeln!(out, ";")?;
        }
        Instruction::Compare(cmp, lhs, rhs) => {
            write!(out, "flag = ")?;
            if cmp.negated {
                write!(out, "!")?;
            }
            write!(out, "(")?;
            emit_expr(lhs, out)?;
            match cmp.ty {
                ComparisonType::Eq => write!(out, " == ")?,
                ComparisonType::Lt => write!(out, " < ")?,
                ComparisonType::Gt => write!(out, " > ")?,
            }
            emit_expr(rhs, out)?;
            writeln!(out, ");")?;
        }
        Instruction::Push(ch, expr) => {
            write!(out, "PUSH({}, ", ch.varname())?;
            emit_expr(expr, out)?;
            writeln!(out, ");")?;
        }
        Instruction::Pop(ch) => {
            writeln!(out, "POP({});", ch.varname())?;
        }
        Instruction::InputCharacter(ch) => {
            writeln!(out, "{}.value = getchar();", ch.varname())?;
        }
        Instruction::InputNumber(ch) => {
            writeln!(out, "{}.value = readint();", ch.varname())?;
        }
        Instruction::OutputCharacter(ch) => {
            writeln!(out, "putchar({}.value);", ch.varname())?;
        }
        Instruction::OutputNumber(ch) => {
            writeln!(out, "printf(\"%d\", {}.value);", ch.varname())?;
        }
        Instruction::Goto(BlockId(block)) => {
            writeln!(out, "goto bb{block};")?;
        }
    }

    Ok(())
}

fn emit_expr(expr: &Expr, out: &mut PrettyPrinter<'_, impl Write>) -> io::Result<()> {
    match expr {
        Expr::Character(ch) => write!(out, "{}.value", ch.varname())?,
        Expr::Const(n) => write!(out, "{n}")?,
        Expr::UnOp(op, arg) => {
            match op {
                UnOp::Twice => write!(out, "(2 * ")?,
                UnOp::Square => write!(out, "square(")?,
                UnOp::Cube => write!(out, "cube(")?,
                UnOp::Sqrt => write!(out, "isqrt(")?,
                UnOp::Factorial => write!(out, "factorial(")?,
            }

            emit_expr(arg, out)?;
            write!(out, ")")?;
        }
        Expr::BinOp(op, lhs, rhs) => {
            write!(out, "(")?;
            emit_expr(lhs, out)?;
            match op {
                BinOp::Add => write!(out, " + ")?,
                BinOp::Sub => write!(out, " - ")?,
                BinOp::Mul => write!(out, " * ")?,
                BinOp::Div => write!(out, " / ")?,
                BinOp::Mod => write!(out, " % ")?,
            }
            emit_expr(rhs, out)?;
            write!(out, ")")?;
        }
    }

    Ok(())
}
