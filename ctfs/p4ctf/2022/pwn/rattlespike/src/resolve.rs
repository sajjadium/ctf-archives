//! This module computes the set of characters present on stage for each point
//! in the program, thus resolving pronouns at compile time. In some cases,
//! basic blocks must be duplicated to do this.

use crate::ErrorSink;
use crate::ast::*;
use crate::classify::CharacterId;
use crate::verify::{SceneAddress, VerifiedPlay};
use std::fmt::Write;
use std::collections::{BTreeSet, BTreeMap, HashMap};
use codemap::{Span, Spanned};

#[derive(Clone, Copy, Debug)]
pub struct BlockId(pub usize);

#[derive(Clone, Debug)]
pub enum Expr {
    Character(CharacterId),
    Const(i32),
    UnOp(UnOp, Box<Expr>),
    BinOp(BinOp, Box<Expr>, Box<Expr>),
}

#[derive(Clone, Debug)]
pub enum Instruction {
    Assign(CharacterId, Expr),
    Compare(Comparison, Expr, Expr),
    Push(CharacterId, Expr),
    Pop(CharacterId),
    InputCharacter(CharacterId),
    InputNumber(CharacterId),
    OutputCharacter(CharacterId),
    OutputNumber(CharacterId),
    Goto(BlockId),
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Condition {
    Always,
    IfTrue,
    IfFalse,
}

#[derive(Clone, Debug)]
pub struct Block {
    pub instructions: Vec<(Condition, Instruction)>,
    pub next: EndAction,
}

#[derive(Clone, Copy, Debug)]
pub enum EndAction {
    Goto(BlockId),
    ExitProgram,
    Unreachable,
}

#[derive(Clone, Copy, Debug)]
enum Presence {
    OnStage(Span),
    // to prevent error spam
    PretendTheyreHere,
    Left(Span),
}

struct Resolver {
    required: Vec<(SceneAddress, BTreeMap<CharacterId, Presence>)>,
    id_for: HashMap<(SceneAddress, BTreeSet<CharacterId>), BlockId>,
}

impl Resolver {
    fn block_id_for(&mut self, scene: SceneAddress, characters: &BTreeMap<CharacterId, Presence>) -> BlockId {
        let present: BTreeSet<CharacterId> = characters.iter()
            .filter(|&(_, &present)| matches!(present, Presence::OnStage(_)))
            .map(|(&ch, _)| ch).collect();
        let state = (scene, present);

        if let Some(&bid) = self.id_for.get(&state) {
            bid
        } else {
            let bid = BlockId(self.required.len());
            self.required.push((scene, characters.clone()));
            self.id_for.insert(state, bid);
            bid
        }
    }
}

struct StageState<'a> {
    e: &'a mut ErrorSink,
    characters: &'a BTreeMap<CharacterId, Presence>,
    speaker: CharacterId,
    reported_bad_you: bool,
}

impl<'a> StageState<'a> {
    fn second_person(&mut self, span: Span) -> Option<CharacterId> {
        if self.characters.iter().any(|(_, &present)| matches!(present, Presence::PretendTheyreHere)) {
            self.reported_bad_you = true;
        }

        let present: Vec<CharacterId> = self.characters.iter()
            .filter(|&(_, &present)| matches!(present, Presence::OnStage(_)))
            .map(|(&ch, _)| ch)
            .filter(|&ch| ch != self.speaker)
            .collect();

        match &present[..] {
            &[] => {
                if !self.reported_bad_you {
                    self.reported_bad_you = true;
                    self.e
                        .error(format!("{} is speaking into the void", self.speaker))
                        .primary(span, "there's nobody else on stage".to_owned())
                        .emit();
                }
                None
            }
            &[person] => Some(person),
            many => {
                let mut others = String::new();
                for (i, person) in many.iter().enumerate() {
                    match i {
                        0 => write!(others, "{person}").unwrap(),
                        i if i == many.len() - 1 => write!(others, " or {person}").unwrap(),
                        _ => write!(others, ", {person}").unwrap(),
                    }
                }

                if !self.reported_bad_you {
                    self.reported_bad_you = true;
                    self.e
                        .error(format!("ambiguous listener"))
                        .primary(span, format!("is this referring to {others}?"))
                        .emit();
                }
                None
            }
        }
    }

    fn resolve_pronoun(&mut self, p: Spanned<Pronoun>) -> Option<CharacterId> {
        match p.node {
            Pronoun::FirstPerson => Some(self.speaker),
            Pronoun::SecondPerson => self.second_person(p.span),
        }
    }

    fn resolve_value(&mut self, value: &Value) -> Option<Expr> {
        match value {
            &Value::Character(ch) => Some(Expr::Character(ch.0.node)),
            &Value::Pronoun(p) => self.resolve_pronoun(p).map(Expr::Character),
            &Value::Const(n) => Some(Expr::Const(n)),
            Value::UnOp(op, arg) => {
                let arg = self.resolve_value(arg)?;
                Some(Expr::UnOp(*op, Box::new(arg)))
            }
            Value::BinOp(op, lhs, rhs) => {
                let lhs = self.resolve_value(lhs)?;
                let rhs = self.resolve_value(rhs)?;
                Some(Expr::BinOp(*op, Box::new(lhs), Box::new(rhs)))
            }
        }
    }
}

pub fn resolve(e: &mut ErrorSink, play: &VerifiedPlay) -> Vec<Block> {
    let mut blocks: Vec<Block> = vec![];
    let mut reachable_scenes: BTreeSet<SceneAddress> = BTreeSet::new();
    let mut resolver = Resolver {
        required: vec![],
        id_for: HashMap::new(),
    };

    resolver.block_id_for(SceneAddress { act: 1, scene: 1 }, &BTreeMap::new());

    while blocks.len() < resolver.required.len() {
        let (scene, mut on_stage) = resolver.required[blocks.len()].clone();
        reachable_scenes.insert(scene);

        let mut instructions = vec![];
        let mut reachable = true;
        let mut unreachable_span = None;
        for event in &play.get_scene(scene).events {
            if !reachable {
                unreachable_span = match unreachable_span {
                    Some(x) => Some(event.span.merge(x)),
                    None => Some(event.span),
                };

                continue;
            }

            match &event.node {
                Event::Enter(entering) => {
                    for character in entering {
                        if let Some(&Presence::OnStage(span)) = on_stage.get(&character.0.node) {
                            e.error(format!("{character} is already present on stage"))
                                .primary(character.0.span, "can't enter twice".to_owned())
                                .secondary(span, format!("{character} already entered the stage here"))
                                .emit();
                        }

                        on_stage.insert(character.0.node, Presence::OnStage(character.0.span));
                    }
                }
                Event::Exit(exiting) => {
                    if exiting.is_empty() {
                        for character in &play.characters {
                            on_stage.insert(character.0.node, Presence::Left(event.span));
                        }
                    } else {
                        for character in exiting {
                            match on_stage.get(&character.0.node) {
                                Some(Presence::OnStage(_)) => {},
                                Some(Presence::PretendTheyreHere) => {},
                                Some(&Presence::Left(span)) => {
                                    e.error(format!("{character} is not present on stage"))
                                        .primary(character.0.span, "can't leave when not on stage".to_owned())
                                        .secondary(span, format!("{character} already left the stage here"))
                                        .emit();
                                }
                                None => {
                                    e.error(format!("{character} is not present on stage"))
                                        .primary(character.0.span, "can't leave when not present on stage".to_owned())
                                        .emit();
                                }
                            }

                            on_stage.insert(character.0.node, Presence::Left(character.0.span));
                        }
                    }
                }
                Event::Speak(speaker, sentences) => {
                    match on_stage.get(&speaker.0.node) {
                        Some(Presence::OnStage(_)) => {},
                        Some(Presence::PretendTheyreHere) => {},
                        Some(&Presence::Left(span)) => {
                            e.error(format!("{speaker} is not present on stage"))
                                .primary(speaker.0.span, "can't speak when not on stage".to_owned())
                                .secondary(span, format!("{speaker} left the stage here"))
                                .emit();
                            on_stage.insert(speaker.0.node, Presence::PretendTheyreHere);
                        }
                        None => {
                            e.error(format!("{speaker} is not present on stage"))
                                .primary(speaker.0.span, "can't speak when not on stage".to_owned())
                                .emit();
                            on_stage.insert(speaker.0.node, Presence::PretendTheyreHere);
                        }
                    }

                    let mut stage_state = StageState {
                        e,
                        characters: &on_stage,
                        speaker: speaker.0.node,
                        reported_bad_you: false,
                    };

                    for sentence in sentences {
                        if !reachable {
                            unreachable_span = match unreachable_span {
                                Some(x) => Some(sentence.span.merge(x)),
                                None => Some(sentence.span),
                            };

                            continue;
                        }

                        let (cond, inner, instr_span) = match &sentence.node {
                            Sentence::Condition(true, inner) => (Condition::IfTrue, &inner.node, inner.span),
                            Sentence::Condition(false, inner) => (Condition::IfFalse, &inner.node, inner.span),
                            Sentence::Always(inner) => (Condition::Always, inner, sentence.span),
                        };

                        let instr = match inner {
                            &UnconditionalSentence::Goto(target) => {
                                if cond == Condition::Always {
                                    reachable = false;
                                }

                                let target_bid = resolver.block_id_for(target, &on_stage);
                                Instruction::Goto(target_bid)
                            }
                            UnconditionalSentence::Push(value) => {
                                let Some(other) = stage_state.second_person(instr_span) else { continue };
                                let Some(expr) = stage_state.resolve_value(value) else { continue };
                                Instruction::Push(other, expr)
                            }
                            UnconditionalSentence::Pop => {
                                let Some(other) = stage_state.second_person(instr_span) else { continue };
                                Instruction::Pop(other)
                            }
                            UnconditionalSentence::InputCharacter => {
                                let Some(other) = stage_state.second_person(instr_span) else { continue };
                                Instruction::InputCharacter(other)
                            }
                            UnconditionalSentence::InputNumber => {
                                let Some(other) = stage_state.second_person(instr_span) else { continue };
                                Instruction::InputNumber(other)
                            }
                            UnconditionalSentence::OutputCharacter => {
                                let Some(other) = stage_state.second_person(instr_span) else { continue };
                                Instruction::OutputCharacter(other)
                            }
                            UnconditionalSentence::OutputNumber => {
                                let Some(other) = stage_state.second_person(instr_span) else { continue };
                                Instruction::OutputNumber(other)
                            }
                            UnconditionalSentence::Assign(who, value) => {
                                let Some(who) = stage_state.resolve_pronoun(*who) else { continue };
                                let Some(expr) = stage_state.resolve_value(value) else { continue };
                                Instruction::Assign(who, expr)
                            }
                            UnconditionalSentence::Question(lhs, cmp, rhs) => {
                                let Some(lhs) = stage_state.resolve_value(lhs) else { continue };
                                let Some(rhs) = stage_state.resolve_value(rhs) else { continue };
                                Instruction::Compare(cmp.node, lhs, rhs)
                            }
                        };

                        instructions.push((cond, instr));
                    }
                }
            }
        }

        if let Some(unreachable_span) = unreachable_span {
            e.warning("unreachable code".to_owned())
                .primary(unreachable_span, "won't be executed".to_owned())
                .emit();
        }

        let next = if reachable {
            match play.next_after(scene) {
                Some(scene) => EndAction::Goto(resolver.block_id_for(scene, &on_stage)),
                None => EndAction::ExitProgram,
            }
        } else {
            EndAction::Unreachable
        };

        blocks.push(Block {
            instructions,
            next,
        });
    }

    for (&act, scenes) in play.acts.iter() {
        for (&scene, events) in scenes.iter() {
            let scene = SceneAddress { act, scene };
            if !reachable_scenes.contains(&scene) {
                e.warning("unreachable code".to_owned())
                    .primary(events.header_span, "won't be executed".to_owned())
                    .emit();
            }
        }
    }

    blocks
}
