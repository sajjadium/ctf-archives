package jython.parse;

import jython.rts.Interpreter;
import jython.rts.Errors;

import java.util.function.Supplier;

public final class Ast {
    public static record Pos(String curFile, int lineNum, int column, int pos) implements HasPos {
        @Override
        public Pos basePos() { return this; }
    }

    public interface HasPos {
        Pos basePos();
    }

    public sealed interface Stmt extends HasPos {
        record Pass(Pos basePos) implements Stmt {}

        record Expr(Pos basePos, RExpr expr) implements Stmt {}

        record Assignment(Pos basePos, LExpr lvar, RExpr rvar) implements Stmt {}

        record FunctionDef(Pos basePos, String name, String[] args, Stmt[] bodyClause) implements Stmt {}

        record IfStmt(Pos basePos, RExpr cond, Stmt[] thenClause, Stmt[] elseClause) implements Stmt {}

        record WhileStmt(Pos basePos, RExpr cond, Stmt[] bodyClause) implements Stmt {}

        record Import(Pos basePos, String packageName) implements Stmt {};
    }

    public sealed interface LExpr extends HasPos {
        record Qualifier(Pos basePos, RExpr obj, String member) implements LExpr {}

        record Variable(Pos basePos, String name) implements LExpr {}

        record Subscript(Pos basePos, RExpr obj, RExpr ind) implements LExpr {}

        record Deref(Pos basePos, RExpr obj) implements LExpr { }
    }

    public sealed interface RExpr extends HasPos {
        record String(Pos basePos, java.lang.String str) implements RExpr { }

        record Number(Pos basePos, int num) implements RExpr { }

        record Lval(LExpr expr) implements RExpr {
            @Override
            public Pos basePos() { return expr.basePos(); }
        }

        record Ref(Pos basePos, LExpr expr) implements RExpr { }

        record Array(Pos basePos, RExpr[] elems) implements RExpr { }

        default LExpr forceLExpr(Interpreter env) {
            if (this instanceof Lval lv) return lv.expr;
            else throw new Errors.SyntaxError(env, "Expected l-expr, but found r-expr");

        }
    }

    private Ast() {}
}
