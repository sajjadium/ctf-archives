use codemap::Span;
use codemap_diagnostic::{Diagnostic, Level, SpanLabel, SpanStyle};

pub struct ErrorSink {
    pub diagnostics: Vec<Diagnostic>,
    pub error_count: u32,
    pub warning_count: u32,
}

pub struct DiagnosticBuilder<'e> {
    e: &'e mut ErrorSink,
    diag: Diagnostic,
}

impl<'e> DiagnosticBuilder<'e> {
    pub fn emit(self) {
        self.e.emit(self.diag);
    }

    pub fn primary(mut self, span: Span, label: impl Into<Option<String>>) -> Self {
        self.diag.spans.push(SpanLabel {
            span,
            label: label.into(),
            style: SpanStyle::Primary,
        });

        self
    }

    pub fn secondary(mut self, span: Span, label: impl Into<Option<String>>) -> Self {
        self.diag.spans.push(SpanLabel {
            span,
            label: label.into(),
            style: SpanStyle::Secondary,
        });

        self
    }
}

impl ErrorSink {
    pub fn new() -> Self {
        ErrorSink {
            diagnostics: vec![],
            error_count: 0,
            warning_count: 0,
        }
    }

    fn builder(&mut self, level: Level, message: impl Into<String>) -> DiagnosticBuilder<'_> {
        DiagnosticBuilder {
            e: self,
            diag: Diagnostic {
                level,
                message: message.into(),
                code: None,
                spans: vec![],
            },
        }
    }

    pub fn error(&mut self, message: impl Into<String>) -> DiagnosticBuilder<'_> {
        self.builder(Level::Error, message)
    }

    pub fn warning(&mut self, message: impl Into<String>) -> DiagnosticBuilder<'_> {
        self.builder(Level::Warning, message)
    }

    pub fn emit(&mut self, d: Diagnostic) {
        match d.level {
            Level::Error => self.error_count += 1,
            Level::Warning => self.warning_count += 1,
            _ => {}
        }

        self.diagnostics.push(d);
    }

    pub fn show_span(&mut self, s: Span, comment: String) {
        let label = SpanLabel {
            span: s,
            style: SpanStyle::Primary,
            label: None,
        };

        self.emit(Diagnostic {
            level: Level::Note,
            message: comment,
            code: None,
            spans: vec![label],
        });
    }

    pub fn may_continue(&self) -> Result<(), ()> {
        if self.error_count == 0 {
            Ok(())
        } else {
            Err(())
        }
    }
}
