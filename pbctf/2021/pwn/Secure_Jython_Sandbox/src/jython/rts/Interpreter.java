package jython.rts;

import jython.parse.Ast.*;
import jython.rts.Errors.*;
import jython.rts.ObjectTraits.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Stack;
import java.util.function.Supplier;
import java.util.stream.Collectors;

import static java.lang.String.format;
import static jython.rts.Traits.getTraitImplNonNull;

public final class Interpreter {

    public final HashMap<String, Object> locals = new HashMap<>();
    public final Stack<TracebackEntry> tb = new Stack<>();
    public final Builtins builtins = new Builtins(this);

    public Interpreter() {
        locals.put("None", null);
    }

    public TracebackEntry[] mkTB() {
        return tb.toArray(TracebackEntry[]::new);
    }

    public void replaceTB(TracebackEntry ent) {
        tb.pop();
        tb.push(ent);
    }

    public <R> R enterTB(TracebackEntry ent, Supplier<R> fn) {
        tb.push(ent);
        try {
            return fn.get();
        } finally {
            tb.pop();
        }
    }

    public Traits.Tup2<Object, IsReference<Object>> mkRef(LExpr expr, boolean isRH) {
        if (expr instanceof LExpr.Deref deref) {
            if (deref.obj() instanceof RExpr.Ref refd)
                return mkRef(refd.expr(), false);
            else {
                var ref = evalExpr(deref.obj());
                var refTrait = getTraitImplNonNull(this,
                        format("%s object is not a reference", builtins.str(ref.getClass())),
                        IsReference.class, ref.getClass());
                return new Traits.Tup2<>(ref, refTrait);
            }
        } else if (expr instanceof LExpr.Qualifier qual) {
            return builtins.attr(evalExpr(qual.obj()), qual.member());
        } else if (expr instanceof LExpr.Subscript subs) {
            return builtins.item(evalExpr(subs.obj()), evalExpr(subs.ind()));
        } else if (expr instanceof LExpr.Variable var) {
            if (!locals.containsKey(var.name()) && !isRH)
                throw new NamingError(this, String.format("name '%s' is not defined", var.name()));
            return builtins.item(locals, var.name());
        } else {
            throw new AssertionError("Unreachable");
        }
    }

    public Object evalExpr(RExpr expr) {
        if (expr instanceof RExpr.Array arr) {
            return Arrays.stream(arr.elems()).map(this::evalExpr).collect(Collectors.toCollection(ArrayList::new));
        } else if (expr instanceof RExpr.String str) {
            return str.str();
        } else if (expr instanceof RExpr.Number num) {
            return num.num();
        } else if (expr instanceof RExpr.Ref ref) {
            if (ref.expr() instanceof LExpr.Deref derefd) {
                return evalExpr(derefd.obj());
            } else {
                return mkRef(ref.expr(), false).fst();
            }
        } else if (expr instanceof RExpr.Lval lval) {
            var ref = mkRef(lval.expr(), false);
            return ref.snd().__get_deref__(ref.fst());
        }
        throw new AssertionError("Unreachable");
    }

    // Python is too complicated... why don't we simplify it for a change ;)
    public Object executeStmt(Stmt stmt) {
        tb.push(new TracebackEntry(stmt.basePos(), null));
        try {
            if (stmt instanceof Stmt.Pass) {
                return null;
            } else if (stmt instanceof Stmt.Expr sexpr) {
                return evalExpr(sexpr.expr());
            } else if (stmt instanceof Stmt.Assignment asgn) {
                var ref = mkRef(asgn.lvar(), true);
                ref.snd().__set_deref__(ref.fst(), evalExpr(asgn.rvar()));
                return null;
            } else if (stmt instanceof Stmt.FunctionDef) {
                throw new SyntaxError(this, "Unimplemented AST");
            } else if (stmt instanceof Stmt.IfStmt) {
                throw new SyntaxError(this, "Unimplemented AST");
            } else if (stmt instanceof Stmt.WhileStmt) {
                throw new SyntaxError(this, "Unimplemented AST");
            } else if (stmt instanceof Stmt.Import imp) {
                PackageTree.addPackage(imp.packageName());
                Object val = PackageTree.ROOT;
                try {
                    for (var qual : imp.packageName().split("\\."))
                        val = builtins.getattr(val, qual);
                    var qual = imp.packageName().split("\\.")[0];
                    locals.put(qual, builtins.getattr(PackageTree.ROOT, qual));
                    return null;
                } catch (PythonRuntimeException e) {
                    throw new ImportError(this, "No module named " + imp.packageName());
                }
            }

            throw new AssertionError("Unreachable");
        } finally {
            tb.pop();
        }
    }
}
