package jython;

import jython.parse.Ast;
import jython.parse.Lexer;
import jython.parse.Parser;
import jython.rts.Errors;
import jython.rts.Interpreter;
import jython.rts.ObjectTraits;
import org.jline.reader.*;
import org.jline.reader.impl.DefaultParser;

public class Repl {

    private static LineReader reader;

    public static String readLine(String prompt) {
        try {
            return reader.readLine(prompt);
        } catch (EndOfFileException | EOFError e) {
            return null;
        }
    }

    public static void main(String[] args) throws Exception {
        var forced = Class.forName("jython.rts.ObjectTraits");
        var env = new Interpreter();

        DefaultParser lineParser = new DefaultParser();
        lineParser.setQuoteChars(null);
        lineParser.setEscapeChars(null);
        lineParser.setEofOnUnclosedQuote(true);

        reader = LineReaderBuilder.builder()
                .appName("jython")
                .option(LineReader.Option.DISABLE_EVENT_EXPANSION, true)
                .parser(lineParser)
                .build();
        System.out.println(String.format("""
                Jython 2.8.999 (sandbox-standard v1.2)
                [OpenJDK 64-Bit Server VM (%s)] on java%s
                Type "help", "copyright", "credits" or "license" for more information.""",
                System.getProperty("java.vendor"),
                System.getProperty("java.version")));
        env.locals.put("help", new ObjectTraits._Printer("This is only a demo version... no help for you!"));
        env.locals.put("copyright", new ObjectTraits._Printer("Copyright (c) 2021 theKidOfArcrania"));
        env.locals.put("credits", new ObjectTraits._Printer("Not the real Jython(tm)"));
        env.locals.put("license", new ObjectTraits._Printer("TODO"));
        env.locals.put("quit", new ObjectTraits._Printer("Use quit() (TODO!) or Ctrl-D (i.e. EOF) to exit"));
        while (true) {
            try {
                var firstLine = readLine(">>> ");
                if (firstLine == null) break;

                var lexer = new Lexer(env,"<stdin>", firstLine, () -> readLine("... "));
                var parser = new Parser(lexer);
                while (lexer.pos < lexer.lexing.length()) {
                    var stmt = parser.parseStmt();
                    Object value = env.executeStmt(stmt);
                    if (value != null) {
                        System.out.println(env.builtins.repr(value));
                    }
                }
            } catch (UserInterruptException e) {
                System.out.println("KeyboardInterrupt");
            } catch (Errors.PythonRuntimeException e) {
                System.out.print(e.repr());
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
