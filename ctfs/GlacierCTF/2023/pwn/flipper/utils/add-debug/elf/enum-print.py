import sys, re
from optparse import OptionParser

def read_toks():
    data = sys.stdin.read()
    while data:
        data = data.lstrip()
        if data.startswith("//") or data.startswith("#"):
            data = data.split("\n",1)[1]
        elif data.startswith("/*"):
            data = data.split("*/",1)[1]
        elif data.startswith("\"") or data.startswith("'"):
            c = data[0]
            m = re.match(r'%s([^\\%s]|\\.)*%s' % (c,c,c), data)
            yield m.group(0)
            data = data[m.end():]
        else:
            m = re.match(r"[_a-zA-Z0-9]+|[{}();]|[^_a-zA-Z0-9 \n\t\f]+", data)
            yield m.group(0)
            data = data[m.end():]

enums = {}

def do_top_level(toks, ns=[]):
    while toks:
        tok = toks.pop(0)
        if tok == "enum" and toks[0] == "class":
            toks.pop(0)
            name = toks.pop(0)
            # Get to the first token in the body
            while toks.pop(0) != "{":
                pass
            # Consume body and close brace
            do_enum_body("::".join(ns + [name]), toks)
        elif tok == "class":
            name = do_qname(toks)
            # Find the class body, if there is one
            while toks[0] != "{" and toks[0] != ";":
                toks.pop(0)
            # Enter the class's namespace
            if toks[0] == "{":
                toks.pop(0)
                do_top_level(toks, ns + [name])
        elif tok == "{":
            # Enter an unknown namespace
            do_top_level(toks, ns + [None])
        elif tok == "}":
            # Exit the namespace
            assert len(ns)
            return
        elif not ns and tok == "string" and toks[:2] == ["to_string", "("]:
            # Get the argument type and name
            toks.pop(0)
            toks.pop(0)
            typ = do_qname(toks)
            if typ not in enums:
                continue
            arg = toks.pop(0)
            assert toks[0] == ")"

            if typ in options.mask:
                make_to_string_mask(typ, arg)
            else:
                make_to_string(typ, arg)

def fmt_value(typ, key):
    if options.no_type:
        val = key
    else:
        val = "%s%s%s" % (typ, options.separator, key)
    if options.strip_underscore:
        val = val.strip("_")
    return val

def expr_remainder(typ, arg):
    if options.hex:
        return "\"(%s)0x\" + to_hex((int)%s)" % (typ, arg)
    else:
        return "\"(%s)\" + std::to_string((int)%s)" % (typ, arg)

def make_to_string(typ, arg):
    print("std::string")
    print("to_string(%s %s)" % (typ, arg))
    print("{")
    print("        switch (%s) {" % arg)
    for key in enums[typ]:
        if key in options.exclude:
            print("        case %s::%s: break;" % (typ, key))
            continue
        print("        case %s::%s: return \"%s\";" % \
            (typ, key, fmt_value(typ, key)))
    print("        }")
    print("        return %s;" % expr_remainder(typ, arg))
    print("}")
    print

def make_to_string_mask(typ, arg):
    print("std::string")
    print("to_string(%s %s)" % (typ, arg))
    print("{")
    print("        std::string res;")
    for key in enums[typ]:
        if key in options.exclude:
            continue
        print("        if ((%s & %s::%s) == %s::%s) { res += \"%s|\"; %s &= ~%s::%s; }" % \
            (arg, typ, key, typ, key, fmt_value(typ, key), arg, typ, key))
    print("        if (res.empty() || %s != (%s)0) res += %s;" % \
        (arg, typ, expr_remainder(typ, arg)))
    print("        else res.pop_back();")
    print("        return res;")
    print("}")
    print

def do_enum_body(name, toks):
    keys = []
    while True:
        key = toks.pop(0)
        if key == "}":
            assert toks.pop(0) == ";"
            enums[name] = keys
            return
        keys.append(key)
        if toks[0] == "=":
            toks.pop(0)
            toks.pop(0)
        if toks[0] == ",":
            toks.pop(0)
        else:
            assert toks[0] == "}"

def do_qname(toks):
    # Get a nested-name-specifier followed by an identifier
    res = []
    while True:
        res.append(toks.pop(0))
        if toks[0] != "::":
            return "::".join(res)
        toks.pop(0)

parser = OptionParser()
parser.add_option("-x", "--exclude", dest="exclude", action="append",
                  help="exclude FIELD", metavar="FIELD", default=[])
parser.add_option("-u", "--strip-underscore", dest="strip_underscore",
                  action="store_true",
                  help="strip leading and trailing underscores")
parser.add_option("-s", "--separator", dest="separator",
                  help="use SEP between type and field", metavar="SEP",
                  default="::")
parser.add_option("--hex", dest="hex", action="store_true",
                  help="return unknown values in hex", default=False)
parser.add_option("--no-type", dest="no_type", action="store_true",
                  help="omit type")
parser.add_option("--mask", dest="mask", action="append",
                  help="treat TYPE as a bit-mask", metavar="TYPE", default=[])
(options, args) = parser.parse_args()
if args:
    parser.error("expected 0 arguments")

do_top_level(list(read_toks()))
