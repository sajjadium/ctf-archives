package jython.parse;

import jython.rts.Interpreter;
import jython.rts.ObjectTraits;

import java.util.ArrayList;
import java.util.function.Supplier;
import java.util.stream.Collectors;

import static jython.parse.Lexer.TokenType.*;
import static jython.rts.Errors.*;
import static jython.parse.Ast.*;

/* Grammar:
 * stmt -> expr ';' | expr = expr ';' | PASS ';'
 *       | DEF IDEN '(' list(IDEN, ',', 0) ')' ':' stmts
 *       | IF expr ':' stmts
 *       | IF expr ':' stmts ELSE stmts
 *       | IF expr ':' stmt
 *       | IF expr ':' stmt ELSE stmt
 *       | WHILE expr ':' stmts
 *       | IMPORT list(IDEN, '.') ';'
 *
 * stmts -> '{' list(stmt, null) '}'
 *       | stmt
 *
 * expr -> IDEN exprTail
 *       | '*' expr
 *       | '&' expr
 *       | '(' expr ')'
 *       | '[' list(expr, ',', 0) ']' exprTail
 *       | STRING exprTail
 *       | INT exprTail
 *
 * exprTail -> '.' IDEN exprTail | '[' expr ']' exprTail | $
 *
 *
 * FOLLOW(expr) = {']', ')', '{', ';', '=', ','}
 * FOLLOW(exprTail) = {FOLLOW(expr)}
 *
 */

public record Parser(Lexer lexer) implements ObjectTraits.Environmented {

    private SyntaxError perror(String msg) {
        lexer.updateTBEnt();
        return new SyntaxError(getEnv(), msg);
    }

    private SyntaxError perrorOn(String nonTerm) {
        return perror(String.format("Got %s in %s", Parser.this.lexer.curToken(), nonTerm));
    }

    private <E> ArrayList<E> parseList(Supplier<E> parseElem, Lexer.TokenType sep, Lexer.TokenType end, boolean zero) {
        var elems = new ArrayList<E>();
        while (true) {
            if (zero && lexer.curToken() == end) return elems;
            elems.add(parseElem.get());
            var cur = lexer.curToken();
            if (cur == sep) lexer.expect(sep);
            else if (cur == end) return elems;
        }
    }

    @Override
    public Interpreter getEnv() {
        return lexer.env;
    }

    public Stmt[] parseTop() {
        return lexer.enterParseTB(() -> parseList(this::parseStmt, null, EOF, false).toArray(Stmt[]::new));
    }

    public Stmt parseStmt() {
        return lexer.enterParseTB(() -> {
            var startPos = lexer.basePos();
            return switch (lexer.curToken()) {
                // expr ';'
                // expr '=' expr ';'
                case STRING, INT, LPAREN, LBRACK, AMP, TIMES, IDEN -> {
                    var lrexpr = parseExpr();
                    lexer.updateTBEnt();
                    var stmt = switch (lexer.curToken()) {
                        case ASSIGN -> {
                            var lexpr = lrexpr.forceLExpr(getEnv());
                            lexer.expect(ASSIGN);
                            var rexpr = parseExpr();
                            yield new Stmt.Assignment(startPos, lexpr, rexpr);
                        }
                        case EOL -> new Stmt.Expr(startPos, lrexpr);
                        case STRING, EOF, PASS, END_BLOCK, START_BLOCK, DOT, DEF, WHILE, ELSE, IF, AMP, TIMES, WALRUS, COMMA,
                                COLON, RPAREN, LPAREN, RBRACK, LBRACK, INT, IDEN, IMPORT ->
                                throw perrorOn("stmt*");
                    };
                    lexer.expect(EOL);
                    yield stmt;
                }

                // IMPORT list(IDEN, '.') ';'
                case IMPORT -> {
                    lexer.expect(IMPORT);
                    var packageImp = parseList(lexer::expectIden, DOT, EOL, false).stream()
                            .collect(Collectors.joining("."));
                    yield new Stmt.Import(startPos, packageImp);
                }

                // PASS ';'
                case PASS -> {
                    lexer.expect(PASS);
                    lexer.expect(EOL);
                    yield new Stmt.Pass(startPos);
                }

                // DEF IDEN '(' list(IDEN, ',', 0) ')' ':' stmts
                case DEF -> {
                    lexer.expect(DEF);
                    var fnName = lexer.expectIden();
                    lexer.expect(LPAREN);
                    var args = parseList(lexer::expectIden, COMMA, RPAREN, true).toArray(String[]::new);
                    lexer.expect(RPAREN);
                    lexer.expect(COLON);
                    var body = parseStmts();
                    yield new Stmt.FunctionDef(startPos, fnName, args, body);
                }

                // IF expr ':' stmts
                // IF expr ':' stmts ELSE ':' stmts
                case IF -> {
                    lexer.expect(IF);
                    var cond = parseExpr();
                    lexer.expect(COLON);
                    if (lexer.curToken() == EOL) lexer.expect(EOL);
                    var thenClause = parseStmts();
                    var elseClause = new Stmt[0];
                    if (lexer.curToken() == ELSE) {
                        lexer.expect(ELSE);
                        lexer.expect(COLON);
                        elseClause = parseStmts();
                    }
                    yield new Stmt.IfStmt(startPos, cond, thenClause, elseClause);
                }

                // WHILE expr ':' stmts
                case WHILE -> {
                    lexer.expect(WHILE);
                    var cond = parseExpr();
                    lexer.expect(COLON);
                    var bodyClause = parseStmts();
                    yield new Stmt.WhileStmt(startPos, cond, bodyClause);
                }

                // ';'
                case EOL -> {
                    lexer.expect(EOL);
                    yield new Stmt.Pass(startPos);
                }

                // error
                case RBRACK, RPAREN, EOF, DOT, ASSIGN, WALRUS, COMMA, START_BLOCK, END_BLOCK, ELSE, COLON ->
                        throw perrorOn("stmt");
            };
        });
    }

    private Stmt[] parseStmts() {
        if (lexer.curToken == START_BLOCK) {
            lexer.expect(START_BLOCK);
            var ret = parseList(this::parseStmt, null, END_BLOCK, false).toArray(Stmt[]::new);
            lexer.expect(END_BLOCK);
            return ret;
        } else {
            return new Stmt[] { parseStmt() };
        }
    }

    private RExpr parseExpr() {
        var startPos = lexer.basePos();
        return switch (lexer.curToken()) {
            // IDEN lexprTail
            case IDEN -> parseExprTail(new RExpr.Lval(new LExpr.Variable(startPos, lexer.expectIden())));

            // STRING exprTail
            case STRING -> parseExprTail(new RExpr.String(startPos, lexer.expectString()));

            // INT exprTail
            case INT -> parseExprTail(new RExpr.Number(startPos, lexer.expectInt()));

            // '(' expr ')' exprTail
            case LPAREN -> {
                lexer.expect(LPAREN);
                var ret = parseExpr();
                lexer.expect(RPAREN);
                yield parseExprTail(ret);
            }

            // '*' expr
            case TIMES -> {
                lexer.expect(TIMES);
                yield new RExpr.Lval(new LExpr.Deref(startPos, parseExpr()));
            }

            // '&' expr
            case AMP -> {
                var tb = lexer.updateTBEnt();
                lexer.expect(AMP);

                var rexpr = parseExpr();
                lexer.updateTBEntWith(tb);
                yield new RExpr.Ref(startPos, rexpr.forceLExpr(getEnv()));
            }

            // '[' expr [, expr] ']' exprTail
            case LBRACK -> {
                lexer.expect(LBRACK);
                var exprs = parseList(this::parseExpr, COMMA, RBRACK, true);
                lexer.expect(RBRACK);
                yield parseExprTail(new RExpr.Array(startPos, exprs.toArray(RExpr[]::new)));
            }

            // error
            case RBRACK, RPAREN, EOF, DOT, ASSIGN, DEF, WHILE, IF, WALRUS, EOL,
                    COMMA, START_BLOCK, END_BLOCK, ELSE, PASS, COLON, IMPORT ->
                    throw perrorOn("expr");
        };
    }

    private RExpr parseExprTail(RExpr from) {
        var startPos = lexer.basePos();
        return switch (lexer.curToken()) {
            // '.' IDEN lexprTail lexprTail
            case DOT -> {
                lexer.expect(DOT);
                var member = lexer.expectIden();
                yield parseExprTail(new RExpr.Lval(new LExpr.Qualifier(startPos, from, member)));
            }
            // '[' expr ']' lexprTail
            case LBRACK -> {
                lexer.expect(LBRACK);
                var ind = parseExpr();
                lexer.expect(RBRACK);
                yield parseExprTail(new RExpr.Lval(new LExpr.Subscript(startPos, from, ind)));
            }
            // $
            case ASSIGN, RBRACK, RPAREN, START_BLOCK, EOL, COLON, COMMA -> from;
            // Error case
            case STRING, IDEN, INT, LPAREN, DEF, WHILE, IF, AMP, TIMES, WALRUS,
                    END_BLOCK, PASS, ELSE, IMPORT, EOF ->
                    throw perrorOn("exprTail");
        };
    }
}

