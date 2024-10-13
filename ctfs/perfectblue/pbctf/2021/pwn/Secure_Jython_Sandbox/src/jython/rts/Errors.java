package jython.rts;

import jython.parse.Ast;

public final class Errors {
    public static record TracebackEntry(Ast.Pos errorLoc, String codeBuffer) {
        public String repr() {
            var sb = new StringBuilder();
            sb.append(String.format("  File \"%s\", line %d, in <module>\n", errorLoc.curFile(), errorLoc.lineNum()));
            if (codeBuffer != null) {
                var lineTo = codeBuffer.indexOf('\n', errorLoc.pos());
                var line = codeBuffer.substring(errorLoc.pos() - errorLoc.column(),
                        lineTo == -1 ? codeBuffer.length() : lineTo);
                sb.append(String.format("    %s\n    ", line));
                sb.append(" ".repeat(Math.max(0, errorLoc.column())));
                sb.append("^\n");
            }
            return sb.toString();
        }
    }

    public static class PythonRuntimeException extends RuntimeException {
        private final TracebackEntry[] stack;

        public PythonRuntimeException(Interpreter env, String msg) {
            super(msg);
            this.stack = env.mkTB();
        }

        public String repr() {
            var sb = new StringBuilder();
            sb.append("Traceback (most recent call last):\n");
            for (var tbe : stack)
                sb.append(tbe.repr());
            sb.append(getClass().getSimpleName());
            sb.append(": ");
            sb.append(getMessage());
            sb.append('\n');
            return sb.toString();
        }
    }

    public static class ImportError extends PythonRuntimeException {
        public ImportError(Interpreter env, String msg) {
            super(env, msg);
        }
    }

    public static class SyntaxError extends PythonRuntimeException {
        public SyntaxError(Interpreter env, String msg) {
            super(env, msg);
        }
    }

    public static class NamingError extends PythonRuntimeException {
        public NamingError(Interpreter env, String msg) {
            super(env, msg);
        }
    }

    public static class IndentationError extends SyntaxError {
        public IndentationError(Interpreter env, String msg) {
            super(env, msg);
        }
    }

    public static class AttributeError extends PythonRuntimeException {
        private static String msgAttrError(Interpreter env, Class<?> cls, String attr) {
            return String.format("%s object has no attribute '%s'", env.builtins.str(cls), attr);
        }

        public AttributeError(Interpreter env, String msg) {
            super(env, msg);
        }

        public AttributeError(Interpreter env, Class<?> obj, String attr) {
            this(env, msgAttrError(env, obj, attr));
        }
    }

    public static class ItemError extends PythonRuntimeException {
        private static String msgItemError(Interpreter env, Class<?> cls, Object attr) {
            return String.format("%s object has no item '%s'", env.builtins.str(cls), env.builtins.str(attr));
        }

        public ItemError(Interpreter env, String msg) {
            super(env, msg);
        }

        public ItemError(Interpreter env, Class<?> obj, Object item) {
            this(env, msgItemError(env, obj, item));
        }
    }

    public static class TypeError extends PythonRuntimeException {
        private static String msgCoerce(Interpreter env, Class<?> coercedTo) {
            return String.format("Cannot coerce to type '%s'.", env.builtins.str(coercedTo));
        }

        public TypeError(Interpreter env, String msg) {
            super(env, msg);
        }

        public TypeError(Interpreter env, Class<?> coercedTo) {
            super(env, msgCoerce(env, coercedTo));
        }
    }

    public static class JavaError extends RuntimeException {
        public JavaError(Throwable cause) {
            super(cause);
        }
    }

    private Errors() {
    }

}
