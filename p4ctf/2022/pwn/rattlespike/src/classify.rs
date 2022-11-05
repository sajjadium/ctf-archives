use crate::parser::{merge_spans, Token, TokenType};
use codemap::Spanned;
use itertools::put_back_n;
use once_cell::sync::Lazy;
use std::collections::HashMap;
use std::fmt;

#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct CharacterId(u8);

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Tone {
    Positive,
    Neutral,
    Negative,
}

impl fmt::Display for Tone {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Tone::Positive => write!(f, "positive"),
            Tone::Neutral => write!(f, "neutral"),
            Tone::Negative => write!(f, "negative"),
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum WordType {
    Noun(Tone),
    Adjective(Tone),
    Comparative(Tone),
    Character(CharacterId),
}

#[derive(Default)]
struct WordTypes {
    single: Option<WordType>,
    conts: WordTypeMap,
}

#[derive(Default)]
pub struct WordTypeMap(HashMap<&'static str, WordTypes>);

impl WordTypeMap {
    fn new() -> Self {
        Self(HashMap::new())
    }

    fn insert_word(&mut self, word: &'static str, typ: WordType) {
        let mut parts = word.split_whitespace();
        let head = parts.next().unwrap();
        let mut entry = self.0.entry(head);
        for part in parts {
            let map = entry.or_default();
            entry = map.conts.0.entry(part);
        }

        assert!(
            entry.or_default().single.replace(typ).is_none(),
            "collision: {:?}",
            word
        );
    }

    fn get(&self, token: &TokenType<'_>) -> Option<&WordTypes> {
        match token {
            TokenType::Word(s) => self.0.get(*s),
            _ => None,
        }
    }

    // This is quadratic for a bad enough map. Thankfully, the map is hardcoded. I am NOT
    // going to implement Aho-Corasick just for the warm feeling of linear performance for
    // the worst case that will never happen.
    pub fn merge_tokens<'a>(&self, input: impl Iterator<Item = Token<'a>>) -> Vec<Token<'a>> {
        let mut current_map = self;
        let mut withheld = vec![];
        let mut output = vec![];
        // The most recent possible merge end point. Also remembers the length of `withheld`
        // at the time the checkpoint was taken, and thus the number of the tokens the merge
        // would involve.
        //
        // Invariant: the depth of a checkpoint is never 0.
        let mut checkpoint = None;

        let mut input = put_back_n(input);
        while let Some(token) = input.next() {
            let word = if token.node == TokenType::Word("the") {
                &TokenType::Word("The")
            } else {
                &token.node
            };

            if let Some(v) = current_map.get(word) {
                withheld.push(token);
                if let Some(typ) = v.single {
                    // Checkpoint invariant upheld due to the push just above.
                    checkpoint = Some((withheld.len(), typ));
                }

                current_map = &v.conts;
            } else {
                if let Some((depth, typ)) = checkpoint.take() {
                    input.put_back(token);

                    while withheld.len() > depth {
                        // This unwrap is OK due to checkpoint invariant.
                        input.put_back(withheld.pop().unwrap());
                    }

                    let span = merge_spans(withheld.iter().map(|t| t.span)).unwrap();
                    output.push(Spanned {
                        node: TokenType::Merged(typ, withheld),
                        span,
                    });

                    withheld = vec![];
                    current_map = self;
                } else {
                    withheld.push(token);

                    while withheld.len() > 1 {
                        input.put_back(withheld.pop().unwrap());
                    }

                    output.push(withheld.pop().unwrap());
                    current_map = self;
                }
            }
        }

        output
    }
}

static CHARACTER_NAMES: Lazy<Vec<&'static str>> =
    Lazy::new(|| include_str!("character.wordlist").lines().collect());

impl fmt::Debug for CharacterId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "<{}>", CHARACTER_NAMES[self.0 as usize])
    }
}

impl fmt::Display for CharacterId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", CHARACTER_NAMES[self.0 as usize])
    }
}

impl CharacterId {
    pub fn varname(&self) -> String {
        CHARACTER_NAMES[self.0 as usize].replace(' ', "_")
    }
}

pub static WORD_TYPES: Lazy<WordTypeMap> = Lazy::new(|| {
    use Tone::*;
    use WordType::*;

    let mut map = WordTypeMap::new();

    for (i, character) in CHARACTER_NAMES.iter().copied().enumerate() {
        map.insert_word(character, Character(CharacterId(i as u8)));
    }

    let mut with_type = |typ, data: &'static str| {
        for word in data.lines() {
            map.insert_word(word, typ);
        }
    };

    with_type(Noun(Positive), include_str!("positive_noun.wordlist"));
    with_type(Noun(Neutral), include_str!("neutral_noun.wordlist"));
    with_type(Noun(Negative), include_str!("negative_noun.wordlist"));

    with_type(
        Adjective(Positive),
        include_str!("positive_adjective.wordlist"),
    );
    with_type(
        Adjective(Neutral),
        include_str!("neutral_adjective.wordlist"),
    );
    with_type(
        Adjective(Negative),
        include_str!("negative_adjective.wordlist"),
    );

    with_type(
        Comparative(Positive),
        include_str!("positive_comparative.wordlist"),
    );
    with_type(
        Comparative(Negative),
        include_str!("negative_comparative.wordlist"),
    );

    map
});
