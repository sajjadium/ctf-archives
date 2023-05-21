use crate::ast::*;
use crate::classify::{CharacterId, Tone, WordType, WORD_TYPES};
use crate::ErrorSink;
use crate::errors::DiagnosticBuilder;
use codemap::{File, Span, Spanned};
use itertools::Itertools;
use std::iter::Peekable;

pub fn merge_spans<'a>(tokens: impl Iterator<Item = Span>) -> Option<Span> {
    tokens.reduce(|x, y| x.merge(y))
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum TokenType<'a> {
    SentenceEnd,
    QuestionMark,
    Comma,
    Colon,
    LeftBracket,
    RightBracket,
    Word(&'a str),
    Merged(WordType, Vec<Token<'a>>),
}

impl<'a> TokenType<'a> {
    fn character(&self) -> Option<CharacterId> {
        match self {
            TokenType::Merged(WordType::Character(c), _) => Some(*c),
            _ => None,
        }
    }

    fn is_sentence_part(&self) -> bool {
        match self {
            TokenType::Word(_) => true,
            TokenType::Merged(_, _) => true,
            TokenType::Colon => true,
            _ => false,
        }
    }

    fn is_noun(&self) -> bool {
        match self {
            TokenType::Merged(WordType::Noun(_), _) => true,
            _ => false,
        }
    }

    fn is_adjective(&self) -> bool {
        match self {
            TokenType::Merged(WordType::Adjective(_), _) => true,
            _ => false,
        }
    }

    fn is_comparative(&self) -> bool {
        match self {
            TokenType::Merged(WordType::Comparative(_), _) => true,
            _ => false,
        }
    }

    fn tone(&self) -> Option<Tone> {
        match self {
            TokenType::Merged(WordType::Noun(tone), _) => Some(*tone),
            TokenType::Merged(WordType::Adjective(tone), _) => Some(*tone),
            TokenType::Merged(WordType::Comparative(tone), _) => Some(*tone),
            _ => None,
        }
    }

    fn word(&self) -> Option<&'a str> {
        match self {
            TokenType::Word(s) => Some(s),
            _ => None,
        }
    }

    fn sentence_start(&self) -> bool {
        match self {
            TokenType::Word(s) => *s != "Scene" && *s != "Act",
            _ => false,
        }
    }

    fn is(&self, word: &str) -> bool {
        match self {
            TokenType::Word(s) => s.to_lowercase() == word.to_lowercase(),
            _ => false,
        }
    }
}

pub type Token<'a> = Spanned<TokenType<'a>>;

struct Lexer<'a> {
    file: &'a File,
    rest: &'a str,
    pos: u64,
}

impl<'a> Lexer<'a> {
    fn skip(&mut self) {
        self.rest = &self.rest[1..];
        self.pos += 1;
    }

    fn one_byte(&mut self, tok: TokenType<'a>) -> Option<Token<'a>> {
        let span = self.file.span.subspan(self.pos, self.pos + 1);
        self.skip();
        Some(Spanned { node: tok, span })
    }
}

impl<'a> Iterator for Lexer<'a> {
    type Item = Token<'a>;

    fn next(&mut self) -> Option<Self::Item> {
        while self.rest.starts_with(|c: char| c.is_ascii_whitespace()) {
            self.skip();
        }

        match self.rest.chars().next() {
            None => None,
            Some('.') | Some('!') => self.one_byte(TokenType::SentenceEnd),
            Some('?') => self.one_byte(TokenType::QuestionMark),
            Some(',') => self.one_byte(TokenType::Comma),
            Some(':') => self.one_byte(TokenType::Colon),
            Some('[') => self.one_byte(TokenType::LeftBracket),
            Some(']') => self.one_byte(TokenType::RightBracket),
            _ => {
                let split_pred = |c: char| c.is_ascii_whitespace() || ".!?,:[]".contains(c);
                let (tok, rest) = match self.rest.find(split_pred) {
                    Some(pos) => self.rest.split_at(pos),
                    None => (self.rest, ""),
                };

                let begin = self.pos;
                let end = self.pos + tok.len() as u64;
                self.rest = rest;
                self.pos = end;
                Some(Spanned {
                    node: TokenType::Word(tok),
                    span: self.file.span.subspan(begin, end),
                })
            }
        }
    }
}

struct Parser<'a, 'e> {
    file: &'a File,
    tokens: Peekable<std::vec::IntoIter<Token<'a>>>,
    e: &'e mut ErrorSink,
}

// Invariant: if None is returned, an error has been emitted.
impl<'a, 'e> Parser<'a, 'e> {
    fn eof_span(&self) -> Span {
        let x = self.file.span.len();
        self.file.span.subspan(x, x)
    }

    fn eof_error(&mut self, name: &str) {
        let span = self.eof_span();
        self.e
            .error(format!("expected a {}, but the file has ended", name))
            .primary(span, None)
            .emit();
    }

    fn need_token(&mut self, name: &str) -> Option<Token<'a>> {
        match self.tokens.next() {
            Some(tok) => Some(tok),
            None => {
                self.eof_error(name);
                None
            }
        }
    }

    fn need_peek(&mut self, name: &str) -> Option<Token<'a>> {
        if self.tokens.peek().is_some() {
            self.tokens.peek().cloned()
        } else {
            self.eof_error(name);
            None
        }
    }

    fn accept(&mut self) {
        self.tokens.next().unwrap();
    }

    fn expect(&mut self, expected: TokenType, description: &str, name: &str) -> Option<Token<'a>> {
        let token = self.need_token(name)?;
        if token.node != expected {
            self.e
                .error(format!("expected {}", description))
                .primary(token.span, format!("expected {}", name))
                .emit();
            return None;
        }

        Some(token)
    }

    fn try_consume(&mut self, word: &str) -> Option<Token<'a>> {
        if let Some(token) = self.tokens.peek() {
            if token.is(word) {
                return self.tokens.next();
            }
        }

        None
    }

    fn sync(&mut self, expected: impl Fn(&TokenType) -> bool, name: &str, error_occured: bool) -> Option<Token<'a>> {
        let mut error_span = None;
        let report_error = |e: &mut ErrorSink, span| {
            e.error(format!("expected a {}", name))
                .primary(span, None)
                .emit();
        };

        while let Some(token) = self.tokens.next() {
            if expected(&token.node) {
                if !error_occured {
                    if let Some(span) = error_span {
                        report_error(self.e, span);
                    }
                }
                return Some(token);
            } else if let Some(error) = error_span {
                error_span = Some(error.merge(token.span));
            } else {
                error_span = Some(token.span);
            }
        }

        if !error_occured {
            if let Some(span) = error_span {
                report_error(self.e, span);
            } else {
                self.eof_error(name);
            }
        }

        return None;
    }

    fn thou_error(&mut self, span: Span, description: &str) -> DiagnosticBuilder<'_> {
        self.e
            .error(description.to_owned())
            .primary(span, "tsk, Shakespeare would cringe".to_owned())
            .secondary(span, "See https://www.youtu.be/ZchPs0Rzc84".to_owned())
    }

    fn end_of_sentence(&mut self) -> Option<Span> {
        Some(self.sync(|t| t == &TokenType::SentenceEnd, "period", false)?.span)
    }

    fn comment(&mut self, name: &str) -> Option<Span> {
        let span = merge_spans(
            self.tokens
                .peeking_take_while(|c| c.node != TokenType::SentenceEnd)
                .map(|x| x.span),
        );

        match self.tokens.next() {
            Some(x) => {
                assert!(x.node == TokenType::SentenceEnd);
                Some(span.unwrap_or_else(|| x.span.subspan(0, 0)))
            }
            None => {
                if let Some(span) = span {
                    self.e
                        .error(format!("unterminated {}", name))
                        .primary(span, "add a `.` or `!`".to_owned())
                        .emit();
                } else {
                    self.eof_error(name);
                }

                None
            }
        }
    }

    fn character(&mut self) -> Option<Character> {
        let token = self.need_token("character name")?;
        match token.character() {
            Some(c) => Some(Character(token.map_node(|_| c))),
            None => {
                self.e
                    .error(format!("expected a character name"))
                    .primary(token.span, None)
                    .emit();
                None
            }
        }
    }

    fn dramatis_persona(&mut self) -> Option<Character> {
        let character = self.character()?;
        self.expect(
            TokenType::Comma,
            "a comma between character name and description",
            "a comma",
        )?;
        self.comment("character description")?;
        Some(character)
    }

    fn dramatis_personae(&mut self) -> Option<Vec<Character>> {
        let mut characters = vec![];

        while self.tokens.peek().and_then(|t| t.character()).is_some() {
            characters.push(self.dramatis_persona()?);
        }

        Some(characters)
    }

    fn roman_numeral(&mut self, name: &str) -> Option<Spanned<i32>> {
        let number = self.need_token(&format!("{} number", name))?;
        let n = number.word().and_then(roman::from);

        match n {
            Some(n) => Some(number.map_node(|_| n)),
            None => {
                self.e
                    .error(format!("{}s should be numbered in roman numerals", name))
                    .primary(number.span, "not a roman numeral".to_owned())
                    .emit();
                None
            }
        }
    }

    fn rest_of_heading(&mut self, name: &str, token: Token<'_>) -> Option<Spanned<i32>> {
        let n = self.roman_numeral(name)?;

        let colon = self.need_token("colon")?;
        if colon.node != TokenType::Colon {
            self.e
                .error(format!(
                    "expected a colon between {} number and title",
                    name
                ))
                .primary(colon.span, None)
                .emit();
            return None;
        }

        self.comment(&format!("{} title", name))?;
        Some(Spanned {
            node: n.node,
            span: n.span.merge(token.span),
        })
    }

    fn acts(&mut self) -> Option<Vec<Act>> {
        let mut acts = vec![];
        while let Some(token) = self.tokens.next() {
            if token.node != TokenType::Word("Act") {
                let expected = if acts.len() == 0 {
                    "expected 'Act'"
                } else {
                    "expected 'Act' or 'Scene'"
                };

                self.e
                    .error(format!("syntax error"))
                    .primary(token.span, expected.to_owned())
                    .emit();
                break;
            }

            let number = self.rest_of_heading("act", token)?;
            let scenes = self.scenes()?;
            acts.push(Act { number, scenes });
        }

        Some(acts)
    }

    fn scenes(&mut self) -> Option<Vec<Scene>> {
        let mut scenes = vec![];
        while self
            .tokens
            .peek()
            .map(|t| t.node == TokenType::Word("Scene"))
            == Some(true)
        {
            let token = self.tokens.next().unwrap();
            let number = self.rest_of_heading("scene", token)?;
            let events = self.events()?;
            scenes.push(Scene { number, events });
        }

        Some(scenes)
    }

    fn rest_of_didaskalia(&mut self, left_bracket: Token<'_>) -> Option<Spanned<Event>> {
        let command = self.need_token("command")?;
        enum Command {
            Enter,
            Exit,
            Exeunt,
        }
        let cmd = match command.node {
            TokenType::Word("Enter") => Command::Enter,
            TokenType::Word("Exit") => Command::Exit,
            TokenType::Word("Exeunt") => Command::Exeunt,
            TokenType::Word(s) => {
                self.e
                    .error(format!("unknown command: `{}`", s))
                    .primary(
                        command.span,
                        "expected `Enter`, `Exit` or `Exeunt`".to_owned(),
                    )
                    .emit();
                return None;
            }
            _ => {
                self.e
                    .error(format!("expected command"))
                    .primary(command.span, None)
                    .emit();
                return None;
            }
        };

        let characters = self.character_list()?;
        let right_bracket = self.sync(|t| t == &TokenType::RightBracket, "`]`", false)?;

        let span = left_bracket.span.merge(right_bracket.span);
        let event = match cmd {
            Command::Enter => {
                if characters.len() == 0 {
                    self.e
                        .error(format!("`Enter` requires at least one character"))
                        .primary(span, None)
                        .emit();
                }
                Event::Enter(characters)
            }
            Command::Exit => {
                if characters.len() != 1 {
                    self.e
                        .error(format!("`Exit` requires exactly one character"))
                        .primary(command.span, "use the plural: `Exeunt`".to_owned())
                        .emit();
                }
                Event::Exit(characters)
            }
            Command::Exeunt => {
                if characters.len() == 1 {
                    self.e
                        .error(format!("`Exeunt` is plural, but only one character exits"))
                        .primary(command.span, "use `Exit` instead".to_owned())
                        .emit();
                }
                Event::Exit(characters)
            }
        };

        Some(Spanned { node: event, span })
    }

    fn character_separator(&mut self) -> Option<Token<'a>> {
        let tok = self.tokens.peek()?;
        match tok.node {
            TokenType::Comma | TokenType::Word("and") => self.tokens.next(),
            _ => None,
        }
    }

    fn character_list(&mut self) -> Option<Vec<Character>> {
        let mut characters = vec![];
        let mut separators: Vec<Token<'_>> = vec![];
        while self.tokens.peek().and_then(|t| t.character()).is_some() {
            let next = self.character()?;
            characters.push(next);
            match self.character_separator() {
                Some(sep) => separators.push(sep.clone()),
                None => break,
            }

            // Oxford comma
            if separators.last().unwrap().node == TokenType::Comma
                && self.tokens.peek().map(|t| t.node == TokenType::Word("and")) == Some(true)
            {
                if separators.len() == 1 {
                    let comma = separators.last().unwrap();
                    self.e
                        .error(format!("incorrect use of Oxford comma"))
                        .primary(
                            comma.span,
                            "a list with an Oxford comma needs three or more elements".to_owned(),
                        )
                        .emit();
                }

                *separators.last_mut().unwrap() = self.tokens.next().unwrap();
            }
        }

        if characters.len() == separators.len() && !characters.is_empty() {
            let token = self.tokens.peek()?;
            if token.node == TokenType::RightBracket {
                let sep = separators.last().unwrap();
                let sep_name = if sep.node == TokenType::Comma {
                    "this comma"
                } else {
                    "`and`"
                };
                self.e
                    .error(format!("expected a character after {}", sep_name))
                    .primary(sep.span, None)
                    .emit();
            } else {
                self.e
                    .error(format!("unknown character"))
                    .primary(token.span, "expected a character".to_owned())
                    .emit();
            }
        }

        for (i, sep) in separators.iter().enumerate() {
            let (expected, explanation) = if i == separators.len() - 1 {
                (TokenType::Word("and"), "an `and`")
            } else {
                (TokenType::Comma, "a comma")
            };

            if sep.node != expected {
                self.e
                    .error(format!("invalid separator"))
                    .primary(sep.span, format!("this should be {}", explanation))
                    .emit();
            }
        }

        Some(characters)
    }

    fn character_speaks(&mut self) -> Option<Spanned<Event>> {
        let speaker = self.character()?;
        self.expect(
            TokenType::Colon,
            "a colon between character and their line",
            "a colon",
        )?;
        let mut sentences = vec![];
        while self.tokens.peek().map(|t| t.sentence_start()) == Some(true) {
            if let Some(sentence) = self.sentence() {
                sentences.push(sentence);
            } else {
                self.sync(|t| t == &TokenType::SentenceEnd || t == &TokenType::QuestionMark, "period", true);
            }
        }

        let mut span = speaker.0.span;
        if let Some(sentence) = sentences.last() {
            span = span.merge(sentence.span);
        }

        let event = Event::Speak(speaker, sentences);
        Some(Spanned { node: event, span })
    }

    fn sentence(&mut self) -> Option<Spanned<Sentence>> {
        if let Some(if_token) = self.try_consume("If") {
            let so_not = self.need_token("`so` or `not`")?;
            let positive = match so_not.node {
                TokenType::Word("so") => true,
                TokenType::Word("not") => false,
                _ => {
                    self.e
                        .error(format!("expected `so` or `not` after `If`"))
                        .primary(so_not.span, None)
                        .emit();
                    return None;
                }
            };

            self.expect(
                TokenType::Comma,
                &format!("a comma after `If {}`", if positive { "so" } else { "not" }),
                "a comma",
            )?;

            let rest = self.unconditional_sentence()?;
            let span = rest.span.merge(if_token.span);
            Some(Spanned {
                node: Sentence::Condition(positive, rest),
                span,
            })
        } else {
            Some(self.unconditional_sentence()?.map_node(Sentence::Always))
        }
    }

    fn unconditional_sentence(&mut self) -> Option<Spanned<UnconditionalSentence>> {
        let head = self.need_token("sentence")?;
        if head.is("you") || head.is("thou") {
            self.assignment(head)
        } else if head.is("am") || head.is("are") || head.is("art") || head.is("is") {
            self.question(head)
        } else if head.is("let") || head.is("we") {
            self.jump(head)
        } else if head.is("speak") {
            self.speak(head)
        } else if head.is("listen") {
            self.listen(head)
        } else if head.is("open") {
            self.open(head)
        } else if head.is("remember") {
            self.push(head)
        } else if head.is("recall") {
            self.pop(head)
        } else {
            self.e.show_span(head.span, "unimplemented non-assignment sentence".to_owned());
            return None;
        }
    }

    fn push(&mut self, head: Token<'_>) -> Option<Spanned<UnconditionalSentence>> {
        let arg = self.value(false)?;
        let span = self.end_of_sentence()?.merge(head.span);
        Some(Spanned {
            node: UnconditionalSentence::Push(arg),
            span,
        })
    }

    fn pop(&mut self, head: Token<'_>) -> Option<Spanned<UnconditionalSentence>> {
        while self.need_peek("sentence")?.is_sentence_part() {
            self.accept();
        }

        let span = self.end_of_sentence()?.merge(head.span);
        Some(Spanned {
            node: UnconditionalSentence::Pop,
            span,
        })
    }

    fn speak(&mut self, head: Token<'_>) -> Option<Spanned<UnconditionalSentence>> {
        let possessive = self.need_token("object")?;
        if possessive.is("your") || possessive.is("thy") || possessive.is("thine") {
            let mind = self.need_token("object")?;
            if mind.is("mind") {
                if possessive.is("thine") {
                    self.thou_error(possessive.span, "incorrect possessive for 'mind'")
                        .secondary(mind.span, "'mind' starts with a consonant".to_owned())
                        .emit();
                }
            } else if mind.is("heart") {
                self.e
                    .error(format!("you can't 'speak' your heart"))
                    .primary(mind.span, "try 'Open your heart.' for numeric output".to_owned())
                    .emit();
            } else {
                self.e
                    .error(format!("expected 'Speak your mind.'"))
                    .primary(mind.span, "expected 'mind'".to_owned())
                    .emit();
            }

            let span = self.end_of_sentence()?.merge(head.span);
            Some(Spanned {
                node: UnconditionalSentence::OutputCharacter,
                span,
            })
        } else {
            self.e
                .error(format!("expected 'Speak your mind.'"))
                .primary(possessive.span, format!("expected 'your' or 'thy'"))
                .emit();
            None
        }
    }

    fn listen(&mut self, head: Token<'_>) -> Option<Spanned<UnconditionalSentence>> {
        self.expect(TokenType::Word("to"), "'Listen to your heart.'", "'of'")?;

        let possessive = self.need_token("object")?;
        if possessive.is("your") || possessive.is("thy") || possessive.is("thine") {
            let heart = self.need_token("object")?;
            if heart.is("heart") {
                if possessive.is("thine") {
                    self.thou_error(possessive.span, "incorrect possessive for 'heart'")
                        .secondary(heart.span, "'heart' starts with a consonant".to_owned())
                        .emit();
                }
            } else if heart.is("mind") {
                self.e
                    .error(format!("you can't 'Listen to your mind'"))
                    .primary(heart.span, "try 'Open your mind.' for character input".to_owned())
                    .emit();
            } else {
                self.e
                    .error(format!("expected 'Listen to your heart'"))
                    .primary(heart.span, "expected 'heart'".to_owned())
                    .emit();
            }

            let span = self.end_of_sentence()?.merge(head.span);
            Some(Spanned {
                node: UnconditionalSentence::InputNumber,
                span,
            })
        } else {
            self.e
                .error(format!("expected 'Listen to your heart.'"))
                .primary(possessive.span, format!("expected 'your' or 'thy'"))
                .emit();
            None
        }
    }

    fn open(&mut self, head: Token<'_>) -> Option<Spanned<UnconditionalSentence>> {
        let possessive = self.need_token("object")?;
        if possessive.is("your") || possessive.is("thy") || possessive.is("thine") {
            let what = self.need_token("object")?;
            if what.is("mind") {
                if possessive.is("thine") {
                    self.thou_error(possessive.span, "incorrect possessive for 'mind'")
                        .secondary(what.span, "'mind' starts with a consonant".to_owned())
                        .emit();
                }

                let span = self.end_of_sentence()?.merge(head.span);
                Some(Spanned {
                    node: UnconditionalSentence::InputCharacter,
                    span,
                })
            } else if what.is("heart") {
                if possessive.is("thine") {
                    self.thou_error(possessive.span, "incorrect possessive for 'heart'")
                        .secondary(what.span, "'heart' starts with a consonant".to_owned())
                        .emit();
                }

                let span = self.end_of_sentence()?.merge(head.span);
                Some(Spanned {
                    node: UnconditionalSentence::OutputNumber,
                    span,
                })
            } else {
                self.e
                    .error(format!("expected 'mind' or 'heart'"))
                    .primary(what.span, None)
                    .emit();
                None
            }
        } else {
            self.e
                .error(format!("expected 'your' or 'thy'"))
                .primary(possessive.span, None)
                .emit();
            None
        }
    }

    fn jump(&mut self, head: Token<'_>) -> Option<Spanned<UnconditionalSentence>> {
        if head.is("let") {
            self.expect(TokenType::Word("us"), "'let us'", "'us'")?;
        } else if head.is("we") {
            let next = self.need_token("jump")?;
            if !next.is("must") && !next.is("shall") {
                self.e
                    .error(format!("expected 'we must' or 'we shall'"))
                    .primary(next.span, "expected 'must' or 'shall'".to_owned())
                    .emit();
                return None;
            }
        } else {
            unreachable!();
        }

        let direction = self.need_token("jump direction")?;
        let direction = if direction.is("proceed") {
            direction.map_node(|_| GotoDirection::Proceed)
        } else if direction.is("return") {
            direction.map_node(|_| GotoDirection::Return)
        } else {
            self.e
                .error(format!("expected 'proceed' or 'return'"))
                .primary(direction.span, None)
                .emit();
            return None;
        };

        self.expect(TokenType::Word("to"), "a jump target", "'to'")?;

        let target_type = self.need_token("jump target")?;

        let mut target = if target_type.is("act") {
            self.roman_numeral("act")?.map_node(GotoTarget::Act)
        } else if target_type.is("scene") {
            self.roman_numeral("scene")?.map_node(GotoTarget::Scene)
        } else {
            self.e
                .error(format!("not a valid jump target"))
                .primary(target_type.span, format!("expected 'Act' or 'Scene'"))
                .emit();
            return None;
        };

        target.span = target.span.merge(target_type.span);

        let span = self.end_of_sentence()?.merge(head.span);
        Some(Spanned {
            node: UnconditionalSentence::Goto(Goto {
                direction,
                target,
            }),
            span,
        })
    }

    fn assignment(&mut self, head: Token<'_>) -> Option<Spanned<UnconditionalSentence>> {
        let you = Spanned {
            node: Pronoun::SecondPerson,
            span: head.span,
        };
        let maybe_be = self.need_peek("verb")?;
        if maybe_be.is("are") || maybe_be.is("art") {
            if (head.is("you") && maybe_be.is("art")) || (head.is("thou") && maybe_be.is("are")) {
                let span = head.span.merge(maybe_be.span);
                self.thou_error(span, "incorrect form of 'to be'").emit();
            }

            self.accept();

            let maybe_as = self.need_peek("object")?;
            if maybe_as.is("as") {
                self.equality()?;
                let v = self.value(false)?;
                let span = self.end_of_sentence()?.merge(you.span);
                Some(Spanned {
                    node: UnconditionalSentence::Assign(you, v),
                    span,
                })
            } else {
                let v = self.constant()?;
                let span = self.end_of_sentence()?.merge(you.span);
                Some(Spanned {
                    node: UnconditionalSentence::Assign(you, v),
                    span,
                })
            }
        } else {
            let v = self.unarticulated_constant()?;
            let span = self.end_of_sentence()?.merge(you.span);
            Some(Spanned {
                node: UnconditionalSentence::Assign(you, v),
                span,
            })
        }
    }

    fn question(&mut self, head: Token<'_>) -> Option<Spanned<UnconditionalSentence>> {
        let lhs = self.value(true)?;
        let cmp = self.comparison()?;
        let rhs = self.value(true)?;
        let span = self.expect(TokenType::QuestionMark, "a question mark", "a question mark")?.span.merge(head.span);
        Some(Spanned {
            node: UnconditionalSentence::Question(lhs, cmp, rhs),
            span,
        })
    }

    fn comparison(&mut self) -> Option<Spanned<Comparison>> {
        let maybe_not = self.need_peek("comparison")?;
        let negated = if maybe_not.is("not") {
            self.accept();
            true
        } else {
            false
        };

        let head = self.need_peek("comparison")?;
        if head.is("as") {
            let span = self.equality()?.merge(maybe_not.span);
            Some(Spanned {
                node: Comparison {
                    negated,
                    ty: ComparisonType::Eq,
                },
                span,
            })
        } else {
            let cmp = self.comparative()?;
            let than = self.expect(TokenType::Word("than"), "'than' after comparative", "'than'")?;
            Some(Spanned {
                node: Comparison {
                    negated,
                    ty: cmp.node,
                },
                span: than.span.merge(maybe_not.span),
            })
        }
    }

    fn comparative(&mut self) -> Option<Spanned<ComparisonType>> {
        let head = self.need_peek("comparative")?;
        if head.is_comparative() {
            self.accept();
            let ty = match head.tone().unwrap() {
                Tone::Positive => ComparisonType::Gt,
                Tone::Negative => ComparisonType::Lt,
                _ => unreachable!(),
            };

            Some(Spanned {
                node: ty,
                span: head.span,
            })
        } else if head.is("more") || head.is("less") {
            self.accept();
            let adj = self.need_token("adjective")?;
            if !adj.is_adjective() {
                self.e
                    .error(format!("expected adjective"))
                    .primary(adj.span, None)
                    .emit();
                None
            } else {
                let ty = match (adj.tone().unwrap(), head.is("less")) {
                    (Tone::Positive, false) => ComparisonType::Gt,
                    (Tone::Negative, false) => ComparisonType::Lt,
                    (Tone::Positive, true) => ComparisonType::Lt,
                    (Tone::Negative, true) => ComparisonType::Gt,
                    _ => {
                        self.e
                            .error(format!("neutral adjective cannot be used as a comparative"))
                            .primary(adj.span, "neutral adjective".to_owned())
                            .emit();
                        return None;
                    }
                };

                Some(Spanned {
                    node: ty,
                    span: head.span.merge(adj.span),
                })
            }
        } else {
            self.e
                .error(format!("expected comparative"))
                .primary(head.span, None)
                .emit();
            None
        }
    }

    fn equality(&mut self) -> Option<Span> {
        let as1 = self.expect(TokenType::Word("as"), "'as' in comparison", "'as'")?;
        let adjective = self.need_token("adjective")?;
        if !adjective.is_adjective() {
            self.e
                .error(format!("adjective expected in comparison"))
                .primary(adjective.span, "expected an adjective".to_owned())
                .emit();
        }

        let as2 = self.expect(TokenType::Word("as"), "'as' in comparison", "'as'")?;
        Some(as1.span.merge(as2.span))
    }

    fn value(&mut self, subject: bool) -> Option<Spanned<Value>> {
        let head = self.need_peek("value")?;
        if let Some(_) = head.character() {
            let character = self.character()?;
            Some(Spanned {
                node: Value::Character(character),
                span: character.0.span,
            })
        } else if head.is("i") || head.is("me") || head.is("myself") {
            self.accept();
            if !subject && head.is("i") {
                self.e
                    .error(format!("'I' is a subject pronoun and cannot be used as an object"))
                    .primary(head.span, None)
                    .emit();
            } else if subject && !head.is("i") {
                self.e
                    .error(format!("not a subject pronoun — try 'I'"))
                    .primary(head.span, None)
                    .emit();
            }

            Some(Spanned {
                node: Value::Pronoun(Spanned {
                    node: Pronoun::FirstPerson,
                    span: head.span,
                }),
                span: head.span,
            })
        } else if head.is("you") || head.is("yourself") || head.is("thee") || head.is("thyself") || head.is("thou") {
            if !subject && head.is("thou") {
                self.thou_error(head.span, "'thou' is a subject pronoun and cannot be used as an object — try 'thee'")
                    .emit();
            } else if subject && head.is("yourself") {
                self.e
                    .error(format!("'yourself' is not a subject pronoun — try 'you'"))
                    .primary(head.span, None)
                    .emit();
            } else if subject && head.is("thyself") {
                self.e
                    .error(format!("'thyself' is not a subject pronoun — try 'thou'"))
                    .primary(head.span, None)
                    .emit();
            } else if subject && head.is("thee") {
                self.thou_error(head.span, "'thee' is not a subject pronoun — try 'thou'")
                    .emit();
            }

            self.accept();
            Some(Spanned {
                node: Value::Pronoun(Spanned {
                    node: Pronoun::SecondPerson,
                    span: head.span,
                }),
                span: head.span,
            })
        } else if head.is("the") {
            self.accept();
            let operator = self.need_peek("value")?;
            if operator.is("sum") {
                self.accept();
                self.expect(TokenType::Word("of"), "'the sum of'", "'of'")?;
                let lhs = self.value(false)?;
                self.expect(TokenType::Word("and"), "'and' between summands", "'and'")?;
                let rhs = self.value(false)?;
                let span = head.span.merge(rhs.span);
                Some(Spanned {
                    node: Value::BinOp(BinOp::Add, Box::new(lhs), Box::new(rhs)),
                    span,
                })
            } else if operator.is("difference") {
                self.accept();
                self.expect(TokenType::Word("between"), "'the difference between'", "'between'")?;
                let lhs = self.value(false)?;
                self.expect(TokenType::Word("and"), "'and' between minuend and subtrahend", "'and'")?;
                let rhs = self.value(false)?;
                let span = head.span.merge(rhs.span);
                Some(Spanned {
                    node: Value::BinOp(BinOp::Sub, Box::new(lhs), Box::new(rhs)),
                    span,
                })
            } else if operator.is("product") {
                self.accept();
                self.expect(TokenType::Word("of"), "'the product of'", "'of'")?;
                let lhs = self.value(false)?;
                self.expect(TokenType::Word("and"), "'and' between factors", "'and'")?;
                let rhs = self.value(false)?;
                let span = head.span.merge(rhs.span);
                Some(Spanned {
                    node: Value::BinOp(BinOp::Mul, Box::new(lhs), Box::new(rhs)),
                    span,
                })
            } else if operator.is("quotient") {
                self.accept();
                self.expect(TokenType::Word("between"), "'the quotient between'", "'between'")?;
                let lhs = self.value(false)?;
                self.expect(TokenType::Word("and"), "'and' between dividend and divisor", "'and'")?;
                let rhs = self.value(false)?;
                let span = head.span.merge(rhs.span);
                Some(Spanned {
                    node: Value::BinOp(BinOp::Div, Box::new(lhs), Box::new(rhs)),
                    span,
                })
            } else if operator.is("remainder") {
                self.accept();
                self.expect(TokenType::Word("of"), "'the remainder of the quotient between'", "'of'")?;
                self.expect(TokenType::Word("the"), "'the remainder of the quotient between'", "'the'")?;
                self.expect(TokenType::Word("quotient"), "'the remainder of the quotient between'", "'quotient'")?;
                self.expect(TokenType::Word("between"), "'the remainder of the quotient between'", "'between'")?;
                let lhs = self.value(false)?;
                self.expect(TokenType::Word("and"), "'and' between dividend and divisor", "'and'")?;
                let rhs = self.value(false)?;
                let span = head.span.merge(rhs.span);
                Some(Spanned {
                    node: Value::BinOp(BinOp::Mod, Box::new(lhs), Box::new(rhs)),
                    span,
                })
            } else if operator.is("square") {
                self.accept();
                let maybe_root = self.need_peek("operator")?;
                if maybe_root.is("root") {
                    self.accept();
                    self.expect(TokenType::Word("of"), "'the square root of'", "'of'")?;
                    let arg = self.value(false)?;
                    let span = head.span.merge(arg.span);
                    Some(Spanned {
                        node: Value::UnOp(UnOp::Sqrt, Box::new(arg)),
                        span,
                    })
                } else {
                    self.expect(TokenType::Word("of"), "'the square of'", "'of'")?;
                    let arg = self.value(false)?;
                    let span = head.span.merge(arg.span);
                    Some(Spanned {
                        node: Value::UnOp(UnOp::Square, Box::new(arg)),
                        span,
                    })
                }
            } else if operator.is("cube") {
                self.accept();
                self.expect(TokenType::Word("of"), "'the cube of'", "'of'")?;
                let arg = self.value(false)?;
                let span = head.span.merge(arg.span);
                Some(Spanned {
                    node: Value::UnOp(UnOp::Cube, Box::new(arg)),
                    span,
                })
            } else if operator.is("factorial") {
                self.accept();
                self.expect(TokenType::Word("of"), "'the factorial of'", "'of'")?;
                let arg = self.value(false)?;
                let span = head.span.merge(arg.span);
                Some(Spanned {
                    node: Value::UnOp(UnOp::Factorial, Box::new(arg)),
                    span,
                })
            } else {
                // the CONSTANT - we already consumed "the" so we can't use self.constant()
                // here
                if let Some(mut constant) = self.unarticulated_constant() {
                    constant.span = constant.span.merge(head.span);
                    Some(constant)
                } else {
                    None
                }
            }
        } else if head.is("twice") {
            self.accept();
            let arg = self.value(false)?;
            let span = head.span.merge(arg.span);
            Some(Spanned {
                node: Value::UnOp(UnOp::Twice, Box::new(arg)),
                span,
            })
        } else {
            self.constant()
        }
    }

    fn constant(&mut self) -> Option<Spanned<Value>> {
        let next = self.need_peek("constant")?;
        if next.is("nothing") || next.is("zero") {
            Some(self.tokens.next().unwrap().map_node(|_| Value::Const(0)))
        } else if next.is("a") || next.is("an") || next.is("the") || next.is("my") || next.is("mine") || next.is("thy") || next.is("thine") || next.is("your") || next.is("his") || next.is("her") || next.is("its") || next.is("their") {
            let article = self.tokens.next().unwrap();
            if let Some(mut constant) = self.unarticulated_constant() {
                constant.span = constant.span.merge(article.span);
                Some(constant)
            } else {
                None
            }
        } else {
            if let Some(constant) = self.unarticulated_constant() {
                self.e
                    .error(format!("articulate is needed"))
                    .primary(next.span, format!("try 'the'"))
                    .emit();
                Some(constant)
            } else {
                None
            }
        }
    }

    fn unarticulated_constant(&mut self) -> Option<Spanned<Value>> {
        let mut adjectives = vec![];
        while self.tokens.peek().map(|t| t.is_adjective()) == Some(true) {
            let adj = self.tokens.next().unwrap();
            let tone = adj.map_node(|x| x.tone().unwrap());
            adjectives.push(tone);
        }

        let noun = self.need_token("noun")?;
        if !noun.is_noun() {
            self.e
                .error(format!("expected a noun or adjective in constant value"))
                .primary(noun.span, "neither a noun nor adjective".to_owned())
                .emit();
            return None;
        }

        let tone = noun.tone().unwrap();
        let disallowed = match tone {
            Tone::Positive | Tone::Neutral => Tone::Negative,
            Tone::Negative => Tone::Positive,
        };

        for adj in &adjectives {
            if adj.node == disallowed {
                self.e
                    .error(format!("a {} noun cannot be described with a {} adjective",
                            tone, disallowed))
                    .primary(adj.span, format!("{} adjective", disallowed))
                    .secondary(noun.span, format!("{} noun", tone))
                    .emit();
            }
        }

        let mut span = noun.span;
        if let Some(adj) = adjectives.first() {
            span = span.merge(adj.span);
        }

        let base = if tone == Tone::Negative { -1 } else { 1 };

        Some(Spanned {
            node: Value::Const(base << adjectives.len()),
            span,
        })
    }

    fn events(&mut self) -> Option<Vec<Spanned<Event>>> {
        let mut events = vec![];
        while let Some(token) = self.tokens.peek() {
            match token.node {
                TokenType::LeftBracket => {
                    let token = self.tokens.next().unwrap();
                    events.extend(self.rest_of_didaskalia(token));
                }
                TokenType::Merged(WordType::Character(_), _) => {
                    events.extend(self.character_speaks());
                }
                _ => break,
            }
        }
        Some(events)
    }
}

fn lex<'a>(src: &'a File) -> Vec<Token<'a>> {
    let lexer = Lexer {
        file: src,
        rest: src.source(),
        pos: 0,
    };

    WORD_TYPES.merge_tokens(lexer)
}

pub(crate) fn parse<'a>(e: &mut ErrorSink, src: &'a File) -> Option<Play> {
    let tokens = lex(src);

    let mut parser = Parser {
        file: src,
        tokens: tokens.into_iter().peekable(),
        e,
    };

    let title = parser.comment("title")?;
    let characters = parser.dramatis_personae()?;
    let acts = parser.acts()?;

    Some(Play {
        title,
        characters,
        acts,
    })
}
