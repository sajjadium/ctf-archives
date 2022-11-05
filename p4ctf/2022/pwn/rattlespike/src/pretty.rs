use std::io;
use std::io::Write;

pub struct PrettyPrinter<'a, W> {
    at_line_begin: bool,
    indent: u32,
    writer: &'a mut W,
}

impl<'a, W: Write> PrettyPrinter<'a, W> {
    pub fn new(writer: &'a mut W) -> Self {
        PrettyPrinter {
            at_line_begin: true,
            indent: 0,
            writer,
        }
    }

    fn print_indent(&mut self) -> io::Result<()> {
        if self.at_line_begin {
            let indent = vec![b' '; self.indent as usize];
            self.writer.write(&indent)?;
            self.at_line_begin = false;
        }

        Ok(())
    }

    pub fn indented(&mut self) -> PrettyPrinter<'_, W> {
        assert!(self.at_line_begin);
        PrettyPrinter {
            at_line_begin: true,
            indent: self.indent + 4,
            writer: self.writer,
        }
    }
}

impl<'a, W: Write> Write for PrettyPrinter<'a, W> {
    fn write(&mut self, mut buf: &[u8]) -> io::Result<usize> {
        let mut total = 0;
        while let Some(newline_pos) = buf.iter().position(|&b| b == b'\n') {
            self.print_indent()?;
            total += self.writer.write(&buf[0..=newline_pos])?;
            self.at_line_begin = true;
            buf = &buf[newline_pos + 1 .. buf.len()];
        }

        if buf.len() != 0 {
            self.print_indent()?;
            total += self.writer.write(buf)?;
        }

        Ok(total)
    }

    fn flush(&mut self) -> io::Result<()> {
        self.writer.flush()
    }
}

pub trait PrettyPrint {
    fn print<W: Write>(&self, p: &mut PrettyPrinter<'_, W>) -> io::Result<()> ;
}

#[allow(dead_code)]
pub fn pretty(object: &impl PrettyPrint) {
    object.print(&mut PrettyPrinter::new(&mut std::io::stdout().lock())).unwrap();
}
