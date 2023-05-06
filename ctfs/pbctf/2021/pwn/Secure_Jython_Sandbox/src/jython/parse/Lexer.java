package jython.parse;

import jython.rts.Interpreter;
import jython.rts.ObjectTraits.Environmented;

import java.util.*;
import java.util.function.BiFunction;
import java.util.function.Supplier;

import static jython.parse.Lexer.TokenType.*;
import static jython.rts.Errors.*;

public final class Lexer implements Ast.HasPos, Environmented {
    public enum TokenType {
        STRING, IDEN, INT, LBRACK, RBRACK, LPAREN, RPAREN, COMMA, EOL, WALRUS, TIMES, IMPORT,
        AMP, IF, ELSE, WHILE, DEF, ASSIGN, DOT, START_BLOCK, END_BLOCK, PASS, COLON, EOF
    }

    public static record LexerState(boolean wantsIndent, boolean lineBegin, Ast.Pos tokenStart, Ast.Pos curPos,
                                    TokenType curToken, Object curLexeme, IndentBlock[] frameStack, TokenType[] tokens) { }

    public static record IndentBlock(int curLevel, String indent) { }

    public final String curFile;
    public String lexing;
    public boolean inTB;

    public final Interpreter env;
    public final Supplier<String> readMore;
    public final Stack<IndentBlock> frameStack;
    public final Queue<TokenType> tokens;
    public boolean wantsIndent;
    public boolean lineBegin;
    public int lineNum;
    public int column;
    public int pos;
    public Ast.Pos tokenStart;
    public TokenType curToken;
    public Object curLexeme;

    public Lexer(Interpreter env, String curFile, String lexing, Supplier<String> readMore) {
        this.env = env;
        this.curFile = curFile;
        if (!lexing.endsWith("\n")) lexing += '\n';
        this.lexing = lexing;
        this.readMore = readMore;
        this.pos = 0;
        this.column = 0;
        this.lineNum = 1;
        this.wantsIndent = false;
        this.lineBegin = true;
        this.frameStack = new Stack<>();
        this.tokens = new LinkedList<>();
        frameStack.push(new IndentBlock(0, ""));
        this.tokenStart = curPos();
    }


    public LexerState saveState() {
        return new LexerState(wantsIndent, lineBegin, basePos(), curPos(), curToken, curLexeme,
                frameStack.toArray(IndentBlock[]::new), tokens.toArray(TokenType[]::new));
    }

    public void restoreState(LexerState st) {
        tokenStart = st.tokenStart;
        wantsIndent = st.wantsIndent;
        lineBegin = st.lineBegin;
        pos = st.curPos.pos();
        lineNum = st.curPos.lineNum();
        column = st.curPos.column();
        curToken = st.curToken;
        curLexeme = st.curLexeme;
        frameStack.clear();
        frameStack.addAll(Arrays.asList(st.frameStack));
        tokens.clear();
        tokens.addAll(Arrays.asList(st.tokens));
    }

    public TokenType curToken() {
        if (curToken == null) lex();
        return curToken;
    }

    public Ast.Pos basePos() { return tokenStart;}

    public Ast.Pos curPos() { return new Ast.Pos(curFile, lineNum, column, pos); }

    public Object expect(TokenType exp) {
        var tok = curToken();
        curToken = null;
        if (exp != tok)
            throw error(SyntaxError::new, "Expected %s but got %s.", exp, tok);
        return curLexeme;
    }

    public String expectString() {
        return (String)expect(STRING);
    }

    public String expectIden() {
        return (String)expect(IDEN);
    }

    public int expectInt() {
        return (Integer)expect(INT);
    }

    @Override
    public Interpreter getEnv() {
        return env;
    }

    public <R> R enterParseTB(Supplier<R> fn) {
        if (!inTB) {
            var ent = updateTBEnt();
            inTB = true;
            try {
                return env.enterTB(ent, fn);
            } finally {
                inTB = false;
            }
        } else {
            updateTBEnt();
            return fn.get();
        }
    }

    public TracebackEntry updateTBEnt() {
        var tb = new TracebackEntry(basePos(), lexing);
        if (inTB) env.replaceTB(tb);
        return tb;
    }

    public void updateTBEntWith(TracebackEntry tb) {
        if (inTB) env.replaceTB(tb);
    }


    private SyntaxError syntaxError(String fmt, Object... args) { return error(SyntaxError::new, fmt, args); }

    private <E extends PythonRuntimeException> E error(BiFunction<Interpreter, String, E> creator,
                                                       String fmt, Object... args) {
        updateTBEnt();
        return creator.apply(env, String.format(fmt, args));
    }

    private TokenType lex_() {
        boolean lineCont = false;
        while (true) {

            // If we have some cache tokens, use that first.
            if (!tokens.isEmpty()) {
                curLexeme = null;
                return tokens.remove();
            }

            // If we reach end of input
            if (pos >= lexing.length()) {
                // If we are at the beginning of a line, try to read more
                if (pos != lexing.length()) throw new AssertionError();
                pos = lexing.length();
                if (lineBegin) {
                    var nextLine = readMore.get();
                    if (nextLine != null) {
                        if (!nextLine.endsWith("\n"))
                            nextLine += '\n';
                        // Add to lexing input
                        //noinspection StringConcatenationInLoop
                        lexing += nextLine;
                        continue;
                    }
                }

                // Otherwise, we reached EOF
                return EOF;
            }

            // We are at the beginning of a line...
            if (lineBegin) {
                tokenStart = curPos();

                // If we have a line continuation, we don't care about reading whitespaces
                if (lineCont) {
                    lineCont = false;
                    lineBegin = false;
                    continue;
                }

                // Otherwise, try to read as much whitespace as we can, to see how much we indented
                var sb = new StringBuilder();
                lineBegin = false;
                while (pos < lexing.length()) {
                    var ch = lexing.charAt(pos);
                    if (ch == ' ' || ch == '\t') {
                        sb.append(ch);
                        pos++;
                        column++;
                    } else {
                        break;
                    }
                }

                var indent = sb.toString();
                var curIndent = frameStack.peek().indent;

                // Find which level this indent corresponds to
                var level = -1;
                var newLevel = false;
                if (curIndent.startsWith(indent)) {
                    // Outer indentation, or same indentation
                    for (var frame : frameStack) {
                        if (frame.indent.equals(indent))
                            level = frame.curLevel;
                    }
                    if (level == -1)
                        throw error(IndentationError::new, "un-indent does not match any outer indentation level");
                } else if (indent.startsWith(curIndent)) {
                    // Inner indentation
                    level = frameStack.peek().curLevel + 1;
                    newLevel = true;
                } else
                    // Not an outer nor inner indentation
                    throw error(IndentationError::new, "inconsistent usage of spaces and tabs");

                // Update our indent scope
                if (wantsIndent) {
                    if (!newLevel) throw error(IndentationError::new, "expected a indented block");
                    frameStack.push(new IndentBlock(level, indent));
                    wantsIndent = false;
                    return START_BLOCK;
                } else {
                    if (newLevel) throw error(IndentationError::new, "unexpected indent");
                    int pops = 0;
                    while (frameStack.peek().curLevel != level) {
                        frameStack.pop();
                        pops++;
                    }
                    var ret = switch(pops) {
                        case 0 -> null;
                        case 1 -> END_BLOCK;
                        default -> {
                            while (pops --> 1)
                                tokens.add(END_BLOCK);
                            yield END_BLOCK;
                        }
                    };
                    if (ret == null) continue;
                    return ret;
                }
            }

            // Otherwise, just lex this character
            var ch = lexing.charAt(pos);
            tokenStart = curPos();
            pos++;
            column++;
            var typ = switch (ch) {
                // Comment
                case '#' -> {
                    while (pos < lexing.length() && lexing.charAt(pos) != '\n') {
                        pos++;
                        column++;
                    }
                    yield null;
                }

                // Operators/symbols
                case '[' -> LBRACK;
                case ']' -> RBRACK;
                case '(' -> LPAREN;
                case ')' -> RPAREN;
                case '=' -> ASSIGN;
                case '.' -> DOT;
                case ',' -> COMMA;
                case ':' -> {
                    if (pos < lexing.length() && lexing.charAt(pos) == '=') {
                        pos++;
                        column++;
                        yield WALRUS;
                    } else {
                        wantsIndent = true;
                        yield COLON;
                    }
                }
                case '*' -> TIMES;
                case '&' -> AMP;

                // Whitespace
                case ' ', '\r', '\t' -> null;

                // Newline
                case '\n' -> {
                    // We are at the beginning of a line, and probably need to parse indentations.
                    lineNum += 1;
                    column = 0;
                    lineBegin = true;
                    if (wantsIndent) {
                        yield null;
                    } else {
                        yield EOL;
                    }
                }

                // String
                case '"', '\'' -> {
                    char start = ch;
                    var sb = new StringBuilder();
                    var escape = false;
                    while (true) {
                        if (pos >= lexing.length()) throw syntaxError("EOF while reading string");

                        ch = lexing.charAt(pos++);
                        if (escape) {
                            var escCh = switch (ch) {
                                case '\\' -> '\\';
                                case '"' -> '"';
                                case '\'' -> '\'';
                                case '0' -> '\0';
                                case 'n' -> '\n';
                                case 't' -> '\t';
                                case 'r' -> '\r';
                                case 'v' -> (char)0xb;
                                case 'x' -> {
                                    if (pos + 2 > lexing.length())
                                        throw syntaxError("EOF while reading string");
                                    pos += 2;
                                    column += 2;
                                    try {
                                        yield (char)Integer.parseInt(lexing.substring(pos - 2, pos), 16);
                                    } catch (NumberFormatException e) {
                                        throw syntaxError("Illegal hex-code escape in string");
                                    }
                                }
                                default -> throw syntaxError("Illegal escape code: '%c'", ch);
                            };
                            sb.append(escCh);
                            escape = false;
                        } else {
                            if (ch == '\\') {
                                escape = true;
                            } else if (ch == '\r' || ch == '\n') {
                                throw syntaxError("EOL while reading string");
                            } else if (ch == start) {
                                break;
                            } else {
                                sb.append(ch);
                            }
                        }
                    }
                    curLexeme = sb.toString();
                    yield STRING;
                }

                // Line continuation
                case '\\' -> {
                    if (pos < lexing.length() && lexing.charAt(pos) == '\n') {
                        pos++;
                        column++;
                        lineBegin = true;
                        lineNum += 1;
                        column = 0;
                        lineCont = true;
                        yield null;
                    } else {
                        throw syntaxError("Unexpected character after line-continuation character");
                    }
                }

                default -> {
                    if (Character.isJavaIdentifierStart(ch)) {
                        // Identifiers
                        var startPos = pos - 1;
                        while (pos < lexing.length() && Character.isJavaIdentifierPart(lexing.charAt(pos))) {
                            pos++;
                            column++;
                        }
                        var iden = lexing.substring(startPos, pos);
                        curLexeme = iden;
                        yield switch (iden) {
                            case "def"    -> DEF;
                            case "if"     -> IF;
                            case "else"   -> ELSE;
                            case "pass"   -> PASS;
                            case "while"  -> WHILE;
                            case "import" -> IMPORT;
                            default -> IDEN;
                        };
                    } else if (Character.isDigit(ch)) {
                        // Digits
                        var startPos = pos - 1;
                        while (pos < lexing.length() && Character.isDigit(lexing.charAt(pos))) {
                            pos++;
                            column++;
                        }
                        try {
                            curLexeme = Integer.parseInt(lexing.substring(startPos, pos));
                        } catch (NumberFormatException e) {
                            throw syntaxError("TODO: unimplemented big integers");
                        }
                        yield INT;
                    }

                    // Illegal character
                    throw syntaxError(String.format("Illegal character '%c'", ch));
                }
            };

            if (wantsIndent && typ != null && typ != EOL && typ != COLON) {
                switch (typ) {
                    case STRING, IDEN, EOF, PASS, DOT, ASSIGN, DEF, WHILE, ELSE, IF, AMP, IMPORT, TIMES,
                            WALRUS, COMMA, RPAREN, LPAREN, RBRACK, LBRACK, INT -> wantsIndent = false;
                    case EOL, COLON, START_BLOCK, END_BLOCK -> {}
                }
            }
            if (typ != null) return typ;
        }
    }

    public void lex() {
        curToken = lex_();
    }
}
