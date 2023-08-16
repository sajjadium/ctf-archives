#include "asm.h"
#include "util.h"
#include "tpu.h"

#include <stdarg.h>
#include <stdbool.h>
#include <string.h>
#include <stdint.h>

#define TEXTALPH "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
#define NUMALPH "0123456789"
#define NAMEALPH TEXTALPH NUMALPH
#define WHITESPACE " \t\v\r\n,"

enum asm_tok {
	/* Global */
	TOK_STDIN, TOK_STDOUT, TOK_TPU, TOK_END,

	/* Operands (order like OP_*) */
	TOK_ACC, TOK_NIL, TOK_LEFT, TOK_RIGHT, TOK_UP,
	TOK_DOWN, TOK_ANY, TOK_LAST, TOK_LIT, TOK_NAME,

	/* Instructions (order like INST_*) */
	TOK_NOP, TOK_MOV, TOK_SWP, TOK_SAV, TOK_ADD,
	TOK_SUB, TOK_NEG, TOK_XOR, TOK_AND, TOK_JMP,
	TOK_JEQ, TOK_JNE, TOK_JRO, TOK_SHL, TOK_SHR,

	/* Misc */
	TOK_COMMENT, TOK_LABEL, TOK_XPOS, TOK_YPOS, TOK_NL, TOK_EOF
};

struct asm_tokenizer {
	const char *filepath;
	FILE *file;
	enum asm_tok tok;
	char *tokstr;
	size_t lineno, off;
	char linebuf[256];
};

static const char *tok_strs[] = {
	/* Global */
	"stdin", "stdout", "tpu", "end",

	/* Operands (order like OP_*) */
	"acc", "nil", "left", "right", "up", "down",
	"any", "last", NULL, NULL,

	/* Instructions (order like INST_*) */
	"nop", "mov", "swp", "sav", "add",
	"sub", "neg", "xor", "and", "jmp",
	"jeq", "jne", "jro", "shl", "shr",

	/* Misc */
	NULL, NULL, NULL, NULL, NULL, NULL
};

static const char *tok_reprs[] = {
	/* Global */
	"'STDIN'", "'STDOUT'", "'TPU'", "'END'",

	/* Operands (order like OP_*) */
	"'ACC'", "'NIL'", "'LEFT'", "'RIGHT'", "'UP'", "'DOWN'",
	"'ANY'", "'LAST'", "<LIT>", "<NAME>",

	/* Instructions (order like INST_*) */
	"'NOP'", "'MOV'", "'SWP'", "'SAV'", "'ADD'",
	"'SUB'", "'NEG'", "'XOR'", "'AND'", "'JMP'",
	"'JEZ'", "'JNZ'", "'JRO'", "'SHL'", "'SHR'",

	/* Misc */
	"#<COMMENT>", "<LABEL>:", "X<INT>", "Y<INT>", "<NL>", "<EOF>"
};

static bool
is_lit(const char *str)
{
	unsigned long v;
	const char *s;
	char *end;

	if (!strncmp(str, "0b", 2)) {
		for (v = 0, s = str + 2; *s; s++)
			v = (2 * v) + (*s == '1');
	} else {
		v = strtoul(str, &end, 0);
		if (!end || *end) return false;
	}

	return v < 256;
}

static uint8_t
str_to_lit(const char *str)
{
	const char *s;
	unsigned v;

	if (!strncmp(str, "0b", 2)) {
		for (v = 0, s = str + 2; *s; s++)
			v = 2 * v + (*s == '1');
		return (uint8_t) v;
	} else {
		return (uint8_t) strtoul(str, NULL, 0);
	}
}

static enum tpu_port_dir
tok_to_dir(enum asm_tok tok)
{
	return tok - TOK_LEFT + DIR_LEFT;
}

static bool
is_int(const char *str)
{
	char *end;
	long v;

	v = strtol(str, &end, 10);
	if (!end || *end) return false;
	if (v < INT32_MIN || v > INT32_MAX) return false;

	return true;
}

enum tpu_inst_type
tok_to_inst(enum asm_tok tok)
{
	if (tok < TOK_NOP || tok > TOK_SHR) abort();
	return tok - TOK_NOP + INST_NOP;
}

enum tpu_inst_op_type
tok_to_optype(enum asm_tok tok)
{
	if (tok < TOK_ACC || tok > TOK_NAME) abort();
	return tok - TOK_ACC + OP_ACC;
}

struct tpu_inst_op
tok_to_op(struct asm_tokenizer *tokenizer, enum asm_tok tok)
{
	struct tpu_inst_op op;

	op.type = tok_to_optype(tok);
	if (op.type == OP_LIT) {
		op.val.lit = str_to_lit(tokenizer->tokstr);
	} else if (op.type == OP_LABEL) {
		op.val.label = strdup(tokenizer->tokstr);
		if (!op.val.label) die("strdup:");
	}

	return op;
}

static size_t
strlcat_op_name(char *buf, struct tpu_inst_op *op, size_t n)
{
	char hhbuf[4];

	if (op->type == OP_LIT) {
		snprintf(hhbuf, 4, "%hhu", op->val.lit);
		return strdcat(buf, hhbuf, n);
	} else if (op->type == OP_LABEL) {
		return strdcat(buf, op->val.label, n);
	} else {
		return strdcat(buf, op_reprs[op->type], n);
	}
}

size_t
asm_print_inst(char *buf, size_t n, struct tpu_inst *inst)
{
	size_t len;

	len = strdcpy(buf, inst_reprs[inst->type], n);
	if (inst->opcnt >= 1) {
		len += strdcat(buf, " ", n);
		len += strlcat_op_name(buf, &inst->ops[0], n);
	}
	if (inst->opcnt >= 2) {
		len += strdcat(buf, ", ", n);
		len += strlcat_op_name(buf, &inst->ops[1], n);
	}

	return len;
}

static enum asm_tok
tok_next(struct asm_tokenizer *tok)
{
	size_t len;
	char *s;
	int i;

	if (!tok->linebuf[tok->off]) {
		if (feof(tok->file)) return TOK_EOF;
		s = fgets(tok->linebuf, sizeof(tok->linebuf), tok->file);
		if (!s && !feof(tok->file)) die("fgets:");
		if (!s) return TOK_NL;

		len = strlen(s);
		if (len && s[len-1] != '\n' && !feof(tok->file))
			die("load: line %lu too long", tok->lineno);
		if (len && s[len-1] == '\n') s[len-1] = '\0';

		tok->lineno += 1;
		tok->tokstr = s;
		tok->off = 0;
		return TOK_NL;
	}

	s = tok->linebuf + tok->off;
	len = strspn(s, WHITESPACE);
	tok->off += len;
	if (!s[len]) return TOK_NL;
	tok->tokstr = (s += len);

	len = strcspn(s, WHITESPACE);
	tok->off += len;
	if (s[len]) {
		s[len] = '\0';
		tok->off += 1;
	}

	for (i = 0; i <= TOK_EOF; i++) {
		if (tok_strs[i] && !strcasecmp(s, tok_strs[i]))
			return (enum asm_tok) i;
	}

	if (is_lit(s)) {
		return TOK_LIT;
	} else if (*s == '#') {
		tok->off += strlen(tok->linebuf + tok->off);
		return TOK_COMMENT;
	} else if (len && strchr(TEXTALPH, *s)
			&& strspn(s, NAMEALPH) == len-1 && s[len-1] == ':') {
		s[len-1] = '\0';
		return TOK_LABEL;
	} else if (*s == 'X' && is_int(s+1)) {
		return TOK_XPOS;
	} else if (*s == 'Y' && is_int(s+1)) {
		return TOK_YPOS;
	} else if (strchr(TEXTALPH, *s)
			&& strspn(s, NAMEALPH) == strlen(s)) {
		return TOK_NAME;
	} else {
		die("load: line %lu, invalid token '%s'", tok->lineno, s);
	}
}

static enum asm_tok
tok_next_in(struct asm_tokenizer *tokenizer, ...)
{
	va_list ap, cpy;
	enum asm_tok tok;
	bool first;
	int arg;

	tok = tok_next(tokenizer);

	va_copy(cpy, ap);

	va_start(cpy, tokenizer);
	while ((arg = va_arg(cpy, int)) > 0) {
		if (tok == arg) return tok;
	}
	va_end(cpy);

	fprintf(stderr, "tis-as: load: ");
	fprintf(stderr, "line %lu, got tok %s, expected one of (",
		tokenizer->lineno, tok_reprs[tok]);
	first = true;
	va_start(ap, tokenizer);
	while ((arg = va_arg(ap, int)) > 0) {
		if (!first) fputc(',', stderr);
		fputs(tok_reprs[arg], stderr);
		first = false;
	}
	va_end(ap);
	fputs(")\n", stderr);

	exit(1);
}

static void
tpu_validate(struct tpu *tpu)
{
	size_t dst;
	int i;

	for (i = 0; i < tpu->inst_cnt; i++) {
		if (tpu->insts[i].opcnt >= 1
				&& tpu->insts[i].ops[0].type == OP_LABEL) {
			dst = tpu_label_get(tpu, tpu->insts[i].ops[0].val.label);
			if (dst == TPU_MAX_INST)
				die("load: tpu X%i Y%i, label '%s' not defined",
					tpu->x, tpu->y,
					tpu->insts[i].ops[0].val.label);
		}
	}
}

void
tis_load(struct tis *tis, const char *filepath, FILE *tis_stdin, FILE *tis_stdout)
{
	struct asm_tokenizer tokenizer;
	struct tpu_inst_op op1, op2;
	enum tpu_inst_type inst;
	struct tpu *tpu = NULL;
	struct tpu_port *port;
	enum tpu_port_dir stdin_dir, stdout_dir;
	bool stdin_set, stdout_set;
	int stdin_x, stdin_y;
	int stdout_x, stdout_y;
	enum asm_tok tok, optok;
	size_t i;

	tis_deinit(tis);
	tis_init(tis, tis_stdin, tis_stdout);

	stdin_set = stdout_set = false;

	tokenizer.filepath = filepath;
	tokenizer.file = fopen(filepath, "r");
	if (!tokenizer.file) die("load: fopen '%s':", filepath);

	tokenizer.lineno = 0;
	tokenizer.off = 0;
	tokenizer.tokstr = NULL;
	tokenizer.linebuf[tokenizer.off] = '\0';
	while ((tok = tok_next(&tokenizer)) != TOK_EOF) {
		switch (tok) {
		case TOK_STDIN:
			if (tpu || stdin_set) goto disallowed;
			tok_next_in(&tokenizer, TOK_XPOS, -1);
			stdin_x = atoi(tokenizer.tokstr + 1);
			tok_next_in(&tokenizer, TOK_YPOS, -1);
			stdin_y = atoi(tokenizer.tokstr + 1);
			optok = tok_next_in(&tokenizer, TOK_COMMENT,
				TOK_LEFT, TOK_RIGHT, TOK_UP, TOK_DOWN, TOK_NL, -1);
			if (optok != TOK_NL && optok != TOK_COMMENT) {
				stdin_dir = tok_to_dir(optok);
				tok_next_in(&tokenizer, TOK_COMMENT, TOK_NL, -1);
			} else {
				stdin_dir = DIR_UP;
			}
			stdin_set = true;
			break;
		case TOK_STDOUT:
			if (tpu || stdout_set) goto disallowed;
			tok_next_in(&tokenizer, TOK_XPOS, -1);
			stdout_x = atoi(tokenizer.tokstr + 1);
			tok_next_in(&tokenizer, TOK_YPOS, -1);
			stdout_y = atoi(tokenizer.tokstr + 1);
			optok = tok_next_in(&tokenizer, TOK_COMMENT,
				TOK_LEFT, TOK_RIGHT, TOK_UP, TOK_DOWN, TOK_NL, -1);
			if (optok != TOK_NL && optok != TOK_COMMENT) {
				stdout_dir = tok_to_dir(optok);
				tok_next_in(&tokenizer, TOK_COMMENT, TOK_NL, -1);
			} else {
				stdout_dir = DIR_DOWN;
			}
			stdout_set = true;
			break;
		case TOK_TPU:
			if (tpu) goto disallowed;
			tpu = tis_add_tpu(tis);
			tpu_init(tpu);
			tpu->tis = tis;
			tok_next_in(&tokenizer, TOK_XPOS, -1);
			tpu->x = atoi(tokenizer.tokstr + 1);
			tok_next_in(&tokenizer, TOK_YPOS, -1);
			tpu->y = atoi(tokenizer.tokstr + 1);
			tok_next_in(&tokenizer, TOK_COMMENT, TOK_NL, -1);
			if (!tpu_map_add(&tis->tpu_map, tpu))
				die("load: duplicate tpu location X%i Y%i",
					tpu->x, tpu->y);
			break;
		case TOK_END:
			if (!tpu) goto disallowed;
			tpu_validate(tpu);
			tpu = NULL;
			tok_next_in(&tokenizer, TOK_COMMENT, TOK_NL, -1);
			break;
		case TOK_NOP: case TOK_MOV: case TOK_SWP: case TOK_SAV:
		case TOK_ADD: case TOK_SUB: case TOK_NEG: case TOK_XOR:
		case TOK_AND: case TOK_JMP: case TOK_JEQ: case TOK_JNE:
		case TOK_JRO: case TOK_SHL: case TOK_SHR:
			if (!tpu) goto disallowed;
			inst = tok_to_inst(tok);

			optok = tok_next_in(&tokenizer, TOK_ACC,
				TOK_NIL, TOK_LEFT, TOK_RIGHT, TOK_UP,
				TOK_DOWN, TOK_ANY, TOK_LAST, TOK_LIT,
				TOK_NAME, TOK_COMMENT, TOK_NL, -1);
			if (optok == TOK_COMMENT || optok == TOK_NL) {
				if (!tpu_add_inst(tpu, inst, 0, op1, op2))
					die("load: line %lu, invalid instruction",
						tokenizer.lineno-1);
				break;
			}
			op1 = tok_to_op(&tokenizer, optok);

			optok = tok_next_in(&tokenizer, TOK_ACC,
				TOK_NIL, TOK_LEFT, TOK_RIGHT, TOK_UP,
				TOK_DOWN, TOK_ANY, TOK_LAST, TOK_LIT,
				TOK_NAME, TOK_COMMENT, TOK_NL, -1);
			if (optok == TOK_COMMENT || optok == TOK_NL) {
				if (!tpu_add_inst(tpu, inst, 1, op1, op2))
					die("load: line %lu, invalid instruction",
						tokenizer.lineno-1);
				break;
			}
			op2 = tok_to_op(&tokenizer, optok);

			tok_next_in(&tokenizer, TOK_COMMENT, TOK_NL, -1);
			if (!tpu_add_inst(tpu, inst, 2, op1, op2))
				die("load: line %lu, invalid instruction",
					tokenizer.lineno-1);
			break;
		case TOK_COMMENT:
			tok_next_in(&tokenizer, TOK_NL, -1);
			break;
		case TOK_LABEL:
			if (!tpu_label_add(tpu, tokenizer.tokstr, tpu->inst_cnt))
				die("load: line %lu, duplicate label (pos)",
					tokenizer.lineno);
			break;
		case TOK_NL:
			break;
		default:
			goto disallowed;
		}
	}

	for (tpu = tis->tpu_vec.tpus, i = 0; i < tis->tpu_vec.cnt; i++, tpu++)
		tpu_init_ports(tpu, &tis->tpu_map);

	for (tpu = tis->tpu_vec.tpus, i = 0; i < tis->tpu_vec.cnt; i++, tpu++) {
		tpu_attach_ports(tpu);

		if (stdin_set && tpu->x == stdin_x && tpu->y == stdin_y) {
			port = &tpu->ports[stdin_dir];
			if (port->dst_tpu) die("load: stdin port in use");
			port->attached = true;
			port->dst_tpu = NULL;
			port->dst_port = &tis->stdin_port;
			port->type = PORT_IN;
			tis->stdin_port.attached = true;
			tis->stdin_port.dst_tpu = tpu;
			tis->stdin_port.dst_port = port;
		}

		if (stdout_set && tpu->x == stdout_x && tpu->y == stdout_y) {
			port = &tpu->ports[stdout_dir];
			if (port->dst_tpu) die("load: stdout port in use");
			port->attached = true;
			port->dst_tpu = NULL;
			port->dst_port = &tis->stdout_port;
			port->type = PORT_OUT;
			tis->stdout_port.attached = true;
			tis->stdout_port.dst_tpu = tpu;
			tis->stdout_port.dst_port = port;
		}
	}

	if (stdin_set && !tis->stdin_port.attached)
		die("load: stdin tpu (X%i Y%i) not found",
			stdin_x, stdin_y);

	if (stdout_set && !tis->stdout_port.attached)
		die("load: stdout tpu (X%i Y%i) not found",
			stdout_x, stdout_y);

	fclose(tokenizer.file);

	return;

disallowed:
	if (tok == TOK_NAME) {
		die("load: line %lu, unexpected token '%s'",
			tokenizer.lineno, tokenizer.tokstr);
	} else {
		die("load: line %lu, token %s not allowed here",
			tokenizer.lineno, tok_reprs[tok]);
	}
}
