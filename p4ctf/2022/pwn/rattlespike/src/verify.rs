//! This module performs the following checks:
//! - acts and scenes are numbered correctly
//! - all used characters have been declared
//! - jumps use the correct direction and point to an existing act or scene
//!
//! The result is an AST with jumps resolved.

use crate::ErrorSink;
use crate::classify::CharacterId;
use crate::pretty::{PrettyPrint, PrettyPrinter};
use crate::ast::*;
use std::collections::{HashSet, BTreeMap};
use std::io;
use std::io::Write;
use codemap::{Span, Spanned};

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct SceneAddress {
    pub act: i32,
    pub scene: i32,
}

impl PrettyPrint for SceneAddress {
    fn print<W: Write>(&self, p: &mut PrettyPrinter<'_, W>) -> io::Result<()> {
        writeln!(p, "jump to act {}, scene {}", self.act, self.scene)
    }
}

#[derive(Clone, Debug)]
pub struct VerifiedPlay {
    pub characters: Vec<Character>,
    pub acts: BTreeMap<i32, BTreeMap<i32, VerifiedScene>>,
}

impl PrettyPrint for VerifiedPlay {
    fn print<W: Write>(&self, p: &mut PrettyPrinter<'_, W>) -> io::Result<()> {
        writeln!(p, "characters: {:?}", self.characters)?;
        for (act, scenes) in self.acts.iter() {
            writeln!(p, "act {act}:")?;
            let mut p = p.indented();
            for (scene, events) in scenes.iter() {
                writeln!(p, "scene {scene}:")?;
                let mut p = p.indented();
                events.print(&mut p)?;
            }
        }

        Ok(())
    }
}

impl VerifiedPlay {
    pub fn get_scene(&self, scene: SceneAddress) -> &VerifiedScene {
        &self.acts[&scene.act][&scene.scene]
    }

    pub fn next_after(&self, scene: SceneAddress) -> Option<SceneAddress> {
        if self.acts[&scene.act].contains_key(&(scene.scene + 1)) {
            Some(SceneAddress {
                act: scene.act,
                scene: scene.scene + 1,
            })
        } else if self.acts.contains_key(&(scene.act + 1)) {
            Some(SceneAddress {
                act: scene.act + 1,
                scene: 1,
            })
        } else {
            None
        }
    }
}

#[derive(Clone, Debug)]
pub struct VerifiedScene {
    pub header_span: Span,
    pub events: Vec<Spanned<Event<SceneAddress>>>,
}

impl PrettyPrint for VerifiedScene {
    fn print<W: Write>(&self, p: &mut PrettyPrinter<'_, W>) -> io::Result<()> {
        for event in &self.events {
            event.print(p)?;
        }

        Ok(())
    }
}

struct Verifier<'e> {
    allowed_characters: HashSet<CharacterId>,
    scene_counts: BTreeMap<i32, i32>,
    e: &'e mut ErrorSink,
}

impl<'e> Verifier<'e> {
    fn has_scene(&self, scene: SceneAddress) -> bool {
        match self.scene_counts.get(&scene.act) {
            Some(&last_scene) => (1..=last_scene).contains(&scene.scene),
            None => false,
        }
    }

    fn verify_character(&mut self, character: Character) {
        if !self.allowed_characters.contains(&character.0.node) {
            // mention each missing character only once
            self.allowed_characters.insert(character.0.node);
            self.e
                .error(format!("{character} is not declared as a character in this play"))
                .primary(character.0.span, "not declared".to_owned())
                .emit();
        }
    }

    fn resolve_goto(&self, current_scene: SceneAddress, target: GotoTarget) -> SceneAddress {
        match target {
            GotoTarget::Act(act) => SceneAddress {
                act,
                scene: 1,
            },
            GotoTarget::Scene(scene) => SceneAddress {
                act: current_scene.act,
                scene,
            },
        }
    }

    fn verify_act(&mut self, act: Act) -> BTreeMap<i32, VerifiedScene> {
        let act_number = act.number.node;
        act.scenes.into_iter()
            .map(|scene| {
                (scene.number.node, self.verify_scene(scene, act_number))
            })
            .collect()
    }

    fn verify_scene(&mut self, scene: Scene, act_number: i32) -> VerifiedScene {
        let scene_number = scene.number.node;
        let current_scene = SceneAddress { act: act_number, scene: scene_number };
        VerifiedScene {
            header_span: scene.number.span,
            events: scene.events.into_iter().map(|event| {
                event.map_node(|ev| self.verify_event(ev, current_scene))
            }).collect()
        }
    }

    fn verify_event(&mut self, event: Event, current_scene: SceneAddress) -> Event<SceneAddress> {
        match event {
            Event::Enter(characters) => {
                for &character in &characters {
                    self.verify_character(character);
                }

                Event::Enter(characters)
            }
            Event::Exit(characters) => {
                for &character in &characters {
                    self.verify_character(character);
                }

                Event::Exit(characters)
            }
            Event::Speak(character, sentences) => {
                self.verify_character(character);
                let sentences = sentences.into_iter().map(|sentence| {
                    sentence.map_node(|s| self.verify_sentence(s, current_scene))
                }).collect();
                Event::Speak(character, sentences)
            }
        }
    }

    fn verify_sentence(&mut self, sentence: Sentence, current_scene: SceneAddress) -> Sentence<SceneAddress> {
        match sentence {
            Sentence::Condition(b, inner) => {
                Sentence::Condition(b, inner.map_node(|s| {
                    self.verify_unconditional_sentence(s, current_scene)
                }))
            }
            Sentence::Always(inner) =>{
                Sentence::Always(self.verify_unconditional_sentence(inner, current_scene))
            }
        }
    }

    fn verify_unconditional_sentence(&mut self, sentence: UnconditionalSentence, current_scene: SceneAddress) -> UnconditionalSentence<SceneAddress> {
        match sentence {
            UnconditionalSentence::Goto(goto) => {
                let target = self.resolve_goto(current_scene, goto.target.node);
                if !self.has_scene(target) {
                    self.e
                        .error(format!("{} does not exist", goto.target.node))
                        .primary(goto.target.span, "doesn't exist".to_owned())
                        .emit();
                }

                match goto.direction.node {
                    GotoDirection::Proceed => {
                        if target <= current_scene {
                            self.e
                                .error(format!("not a forward jump"))
                                .primary(goto.direction.span, "'proceed' indicates a forward jump, but this one goes backwards".to_owned())
                                .emit();
                        }
                    }
                    GotoDirection::Return => {
                        if target > current_scene {
                            self.e
                                .error(format!("not a backward jump"))
                                .primary(goto.direction.span, "'return' indicates a backward jump, but this one goes forwards".to_owned())
                                .emit();
                        }
                    }
                }

                UnconditionalSentence::Goto(target)
            }
            UnconditionalSentence::Push(value) => {
                self.verify_value(&value.node);
                UnconditionalSentence::Push(value)
            }
            UnconditionalSentence::Pop => UnconditionalSentence::Pop,
            UnconditionalSentence::InputCharacter => UnconditionalSentence::InputCharacter,
            UnconditionalSentence::InputNumber => UnconditionalSentence::InputNumber,
            UnconditionalSentence::OutputCharacter => UnconditionalSentence::OutputCharacter,
            UnconditionalSentence::OutputNumber => UnconditionalSentence::OutputNumber,
            UnconditionalSentence::Assign(who, value) => {
                self.verify_value(&value.node);
                UnconditionalSentence::Assign(who, value)
            }
            UnconditionalSentence::Question(lhs, cmp, rhs) => {
                self.verify_value(&lhs.node);
                self.verify_value(&rhs.node);
                UnconditionalSentence::Question(lhs, cmp, rhs)
            }
        }
    }

    fn verify_value(&mut self, value: &Value) {
        match value {
            Value::Character(character) => self.verify_character(*character),
            Value::Pronoun(_) => {}
            Value::Const(_) => {}
            Value::UnOp(_, arg) => self.verify_value(arg),
            Value::BinOp(_, lhs, rhs) => {
                self.verify_value(lhs);
                self.verify_value(rhs);
            }
        }
    }
}

pub fn verify(e: &mut ErrorSink, play: Play) -> Option<VerifiedPlay> {
    let mut scene_counts = BTreeMap::new();

    let mut prev = None;
    for act in &play.acts {
        number_transition(e, prev, act.number, "play", "act");
        if let Some(scenes) = scene_count(e, act) {
            scene_counts.insert(act.number.node, scenes);
        }
        prev = Some(act.number);
    }

    if prev.is_none() {
        e.error(format!("expected at least one act")).emit();
    }

    if e.error_count != 0 {
        return None;
    }

    let mut verifier = Verifier {
        allowed_characters: play.characters.iter().map(|c| c.0.node).collect(),
        scene_counts,
        e,
    };

    let acts = play.acts.into_iter().map(|act| (act.number.node, verifier.verify_act(act))).collect();

    Some(VerifiedPlay {
        characters: play.characters,
        acts,
    })
}

fn scene_count(e: &mut ErrorSink, act: &Act) -> Option<i32> {
    let mut prev = None;
    let act_name = format!("act {}", roman::to(act.number.node).unwrap());
    for scene in &act.scenes {
        number_transition(e, prev, scene.number, &act_name, "scene");
        prev = Some(scene.number);
    }

    if prev.is_none() {
        e.error(format!("{act_name} is empty"))
            .primary(act.number.span, None)
            .emit();
    }

    prev.map(|s| s.node)
}

fn number_transition(e: &mut ErrorSink, prev: Option<Spanned<i32>>, cur: Spanned<i32>, collection_name: &str, element_name: &str) {
    match prev {
        None => {
            if cur.node != 1 {
                e.error(format!("{collection_name} is missing {element_name} I"))
                    .primary(cur.span, format!("expected {element_name} I first"))
                    .emit();
            }
        }
        Some(prev) => {
            let previous = roman::to(prev.node).unwrap();
            let expected = roman::to(prev.node + 1).unwrap();
            if cur.node < prev.node {
                e.error(format!("{element_name} numbers are going backwards"))
                    .primary(cur.span, format!("{element_name} {expected} expected"))
                    .emit();
            } else if cur.node == prev.node {
                e.error(format!("{element_name} {previous} repeats"))
                    .primary(cur.span, format!("{element_name} {expected} expected"))
                    .secondary(prev.span, format!("{element_name} {previous} defined here"))
                    .emit();
            } else if cur.node > prev.node + 1 {
                e.error(format!("{element_name} {expected} skipped"))
                    .primary(cur.span, format!("{element_name} {expected} expected"))
                    .emit();
            }
        }
    }
}
