// Calculator language
// example expression:
// (-b + _sqrt(b^2 - (4*a*c))) / (2*a)
// intrinsic functions are prefixed with an underscore

/* Example program input:
(-b + _sqrt(b^2 - (4*a*c))) / (2*a)
a b c
1 -5 6
1 3 2
1 0 -2
*/

/* Expected output:
3
-1
1.4142135623730951
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "asm_x64.h"

#define MEM_SIZE 1024   /* size of the shared mem[] buffer; bounds-check limit */

enum token_type {
	TOKEN_NUM,
	TOKEN_VAR,
	TOKEN_OP,
	TOKEN_UN_INTRIN,
	TOKEN_BIN_INTRIN,
	TOKEN_COMMA,
	TOKEN_LPAREN,
	TOKEN_RPAREN,
	TOKEN_END,
	TOKEN_ERROR
};

enum operator_type {
	OP_ADD,
	OP_SUB,
	OP_MUL,
	OP_DIV,
	OP_POW
};

/* unary intrinsics: one argument */
enum intrinsic_type {
	INTRIN_SQRT,
	INTRIN_SIN,
	INTRIN_COS,
	INTRIN_EXP,
	INTRIN_LOG,
	INTRIN_LOAD
};

/* binary intrinsics: two arguments */
enum bin_intrinsic_type {
	BININTRIN_MAX,
	BININTRIN_MIN,
	BININTRIN_POW,
	BININTRIN_STORE
};

struct token {
	enum token_type type;
	union {
		double num;
		char var;
		enum operator_type op;
		enum intrinsic_type intrin;
		enum bin_intrinsic_type bin_intrin;
	};
};

struct token_mapping {
	const char *name;
	struct token token;
};

const struct token_mapping operator_mappings[] = {
	{ "+", { .type = TOKEN_OP, .op = OP_ADD } },
	{ "-", { .type = TOKEN_OP, .op = OP_SUB } },
	{ "*", { .type = TOKEN_OP, .op = OP_MUL } },
	{ "/", { .type = TOKEN_OP, .op = OP_DIV } },
	{ "^", { .type = TOKEN_OP, .op = OP_POW } },
	{ "_sin", { .type = TOKEN_UN_INTRIN, .intrin = INTRIN_SIN } },
	{ "_cos", { .type = TOKEN_UN_INTRIN, .intrin = INTRIN_COS } },
	{ "_exp", { .type = TOKEN_UN_INTRIN, .intrin = INTRIN_EXP } },
	{ "_log", { .type = TOKEN_UN_INTRIN, .intrin = INTRIN_LOG } },
	{ "_sqrt", { .type = TOKEN_UN_INTRIN, .intrin = INTRIN_SQRT } },
	{ "_load", { .type = TOKEN_UN_INTRIN, .intrin = INTRIN_LOAD } },
	{ "_max", { .type = TOKEN_BIN_INTRIN, .bin_intrin = BININTRIN_MAX } },
	{ "_min", { .type = TOKEN_BIN_INTRIN, .bin_intrin = BININTRIN_MIN } },
	{ "_pow", { .type = TOKEN_BIN_INTRIN, .bin_intrin = BININTRIN_POW } },
	{ "_store", { .type = TOKEN_BIN_INTRIN, .bin_intrin = BININTRIN_STORE } },
	{ ",", { .type = TOKEN_COMMA } },
	{ "(", { .type = TOKEN_LPAREN } },
	{ ")", { .type = TOKEN_RPAREN } },
	{ NULL, { .type = TOKEN_ERROR } }
};

#define MAX_TOKENS 256
#define MAX_DEPTH  64

static struct token tokens[MAX_TOKENS];
static int ntokens;

static const char *intrinsic_name(enum intrinsic_type intrin)
{
	switch (intrin) {
	case INTRIN_SQRT:
		return "sqrt";
	case INTRIN_SIN:
		return "sin";
	case INTRIN_COS:
		return "cos";
	case INTRIN_EXP:
		return "exp";
	case INTRIN_LOG:
		return "log";
	case INTRIN_LOAD:
		return "load";
	default:
		return "";
	}
}

static const char *bin_intrinsic_name(enum bin_intrinsic_type fn)
{
	switch (fn) {
	case BININTRIN_MAX:
		return "max";
	case BININTRIN_MIN:
		return "min";
	case BININTRIN_POW:
		return "pow";
	case BININTRIN_STORE:
		return "store";
	default:
		return "";
	}
}

static char operator_char(enum operator_type op)
{
	switch (op) {
	case OP_ADD:
		return '+';
	case OP_SUB:
		return '-';
	case OP_MUL:
		return '*';
	case OP_DIV:
		return '/';
	case OP_POW:
		return '^';
	default:
		return '?';
	}
}

static int tokenize(const char *line)
{
	int i = 0, t = 0;

	while (line[i] && line[i] != '\n') {
		int matched = 0;

		if (line[i] == ' ' || line[i] == '\t' ||
		    line[i] == '\r' || line[i] == '\v' ||
		    line[i] == '\f') {
			i++;
			continue;
		}

		if (t >= MAX_TOKENS - 1) {
			fprintf(stderr, "error: too many tokens\n");
			return -1;
		}

		for (const struct token_mapping *mapping = operator_mappings; mapping->name; mapping++) {
			size_t len = strlen(mapping->name);

			if (strncmp(&line[i], mapping->name, len) != 0)
				continue;

			if (mapping->token.type == TOKEN_UN_INTRIN ||
			    mapping->token.type == TOKEN_BIN_INTRIN) {
				char next = line[i + len];

				// the next letter must not be alphanumeric or underscore, to avoid partial matches
				if ((next >= '0' && next <= '9') ||
				    (next >= 'a' && next <= 'z') ||
				    next == '_')
					continue;
			}

			tokens[t] = mapping->token;
			i += len;
			matched = 1;
			break;
		}

		if (matched) {
			t++;
			continue;
		}

		if (line[i] >= '0' && line[i] <= '9') {
			char *end;

			tokens[t].type = TOKEN_NUM;
			tokens[t].num = strtod(&line[i], &end);
			i = end - line;
			t++;
			continue;
		}

		if (line[i] >= 'a' && line[i] <= 'z') {
			tokens[t].type = TOKEN_VAR;
			tokens[t].var = line[i++];
			t++;
			continue;
		}

		fprintf(stderr, "error: unexpected character '%c'\n",
			line[i]);
		return -1;
	}

	tokens[t].type = TOKEN_END;
	t++;
    ntokens = t;
	return t;
}

typedef int ssa_reg_t;

enum ssa_insn_type {
	SSA_BINARY_OP,
	SSA_UNARY_NEGATIVE,
	SSA_UN_INTRIN,
	SSA_BIN_INTRIN,
	SSA_LOAD_LITERAL,
	SSA_LOAD_VAR,
};

struct ssa_insn {
	enum ssa_insn_type type;
	ssa_reg_t dest;
	union {
		struct { ssa_reg_t left, right; enum operator_type op; } binop;
		struct { ssa_reg_t src; } uneg;
		struct { ssa_reg_t src; enum intrinsic_type intrin; } un_intrin;
		struct { ssa_reg_t left, right; enum bin_intrinsic_type fn; } bin_intrin;
		struct { double literal; } load;
		struct { char var; } load_var;
	};
};

#define MAX_SSA 256

static struct ssa_insn ssa_insns[MAX_SSA];
static int nssa;

/* emit a new SSA instruction, and return the dest register */
static ssa_reg_t emit(struct ssa_insn insn)
{
	if (nssa >= MAX_SSA) {
		fprintf(stderr, "error: too many instructions\n");
		exit(1);
	}
	insn.dest = nssa;
	ssa_insns[nssa] = insn;
	return nssa++;
}

static ssa_reg_t parse(void)
{
	ssa_reg_t reg_stack[MAX_DEPTH];
	enum operator_type pending_op[MAX_DEPTH];
	int has_pending[MAX_DEPTH];
	int depth = 0;
	int pos = 0;

	enum intrinsic_type intrin_names[MAX_DEPTH];
	int intrin_at[MAX_DEPTH];

	enum bin_intrinsic_type bin_intrin_names[MAX_DEPTH];
	int bin_intrin_at[MAX_DEPTH];
	ssa_reg_t bin_arg1[MAX_DEPTH];
	int bin_seen_comma[MAX_DEPTH];

	ssa_reg_t input_cache[26];

	int nunary = 0;
	ssa_reg_t reg;

	memset(intrin_at, 0, sizeof(intrin_at));
	memset(has_pending, 0, sizeof(has_pending));
	memset(bin_intrin_at, 0, sizeof(bin_intrin_at));
	memset(bin_seen_comma, 0, sizeof(bin_seen_comma));
	for (int k = 0; k < 26; k++)
		input_cache[k] = -1;

primary:
	/* collect unary +/- */
	while (tokens[pos].type == TOKEN_OP &&
	       (tokens[pos].op == OP_SUB || tokens[pos].op == OP_ADD)) {
		if (tokens[pos].op == OP_SUB)
			nunary++;
		pos++;
	} // todo: buggy parsing of `-(x - y)` as `(-x) - y`

	switch (tokens[pos].type) {
	case TOKEN_NUM:
		reg = emit((struct ssa_insn){
			.type = SSA_LOAD_LITERAL,
			.load.literal = tokens[pos].num,
		});
		pos++;
		goto have_atom;

	case TOKEN_VAR: {
		int idx = tokens[pos].var - 'a';
		if (input_cache[idx] >= 0)
			reg = input_cache[idx]; // already loaded in previous SSA variable
		else
			reg = input_cache[idx] = emit((struct ssa_insn){
				.type = SSA_LOAD_VAR,
				.load_var.var = tokens[pos].var,
			});
		pos++;
		goto have_atom;
	}

	case TOKEN_UN_INTRIN:
		if (depth + 1 >= MAX_DEPTH) {
			fprintf(stderr, "error: nesting too deep\n");
			return -1;
		}
		intrin_names[depth + 1] = tokens[pos].intrin;
		intrin_at[depth + 1] = 1;
		bin_intrin_at[depth + 1] = 0;
		pos++;
		if (tokens[pos].type != TOKEN_LPAREN) {
			fprintf(stderr, "error: expected '(' after intrinsic\n");
			return -1;
		}
		pos++;
		depth++;
		has_pending[depth] = 0;
		goto primary;

	case TOKEN_BIN_INTRIN:
		if (depth + 1 >= MAX_DEPTH) {
			fprintf(stderr, "error: nesting too deep\n");
			return -1;
		}
		bin_intrin_names[depth + 1] = tokens[pos].bin_intrin;
		bin_intrin_at[depth + 1] = 1;
		bin_seen_comma[depth + 1] = 0;
		intrin_at[depth + 1] = 0;
		pos++;
		if (tokens[pos].type != TOKEN_LPAREN) {
			fprintf(stderr, "error: expected '(' after intrinsic\n");
			return -1;
		}
		pos++;
		depth++;
		has_pending[depth] = 0;
		goto primary;

	case TOKEN_LPAREN:
		pos++;
		if (++depth >= MAX_DEPTH) {
			fprintf(stderr, "error: nesting too deep\n");
			return -1;
		}
		has_pending[depth] = 0;
		intrin_at[depth] = 0;
		bin_intrin_at[depth] = 0;
		goto primary;

	default:
		fprintf(stderr, "error: expected expression\n");
		return -1;
	}

have_atom:
	/* emit pending unary negations */
	while (nunary > 0) {
		reg = emit((struct ssa_insn){
			.type = SSA_UNARY_NEGATIVE,
			.uneg.src = reg,
		});
		nunary--;
	}

	/* fold into current depth */
	if (has_pending[depth]) {
		reg = emit((struct ssa_insn){
			.type = SSA_BINARY_OP,
			.binop.op = pending_op[depth],
			.binop.left = reg_stack[depth],
			.binop.right = reg,
		});
		has_pending[depth] = 0;
	}
	reg_stack[depth] = reg;

	/* check what follows */
	if (tokens[pos].type == TOKEN_OP) {
		pending_op[depth] = tokens[pos].op;
		has_pending[depth] = 1;
		pos++;
		goto primary;
	}

	if (tokens[pos].type == TOKEN_COMMA) {
		if (!bin_intrin_at[depth] || bin_seen_comma[depth]) {
			fprintf(stderr, "error: unexpected ','\n");
			return -1;
		}
		bin_arg1[depth] = reg_stack[depth];
		bin_seen_comma[depth] = 1;
		has_pending[depth] = 0;
		pos++;
		goto primary;
	}

	if (tokens[pos].type == TOKEN_RPAREN) {
		if (depth == 0) {
			fprintf(stderr, "error: unexpected ')'\n");
			return -1;
		}
		reg = reg_stack[depth];
		if (intrin_at[depth]) {
			reg = emit((struct ssa_insn){
				.type = SSA_UN_INTRIN,
				.un_intrin.intrin = intrin_names[depth],
				.un_intrin.src = reg,
			});
			intrin_at[depth] = 0;
		} else if (bin_intrin_at[depth]) {
			if (!bin_seen_comma[depth]) {
				fprintf(stderr, "error: binary intrinsic needs 2 arguments\n");
				return -1;
			}
			reg = emit((struct ssa_insn){
				.type = SSA_BIN_INTRIN,
				.bin_intrin.fn = bin_intrin_names[depth],
				.bin_intrin.left = bin_arg1[depth],
				.bin_intrin.right = reg,
			});
			bin_intrin_at[depth] = 0;
		}
		depth--;
		pos++;
		goto have_atom;
	}

	if (tokens[pos].type == TOKEN_END) {
		if (depth != 0) {
			fprintf(stderr, "error: unclosed parenthesis\n");
			return -1;
		}
		return reg_stack[0];
	}

	fprintf(stderr, "error: unexpected token\n");
	return -1;
}

static void print_ssa(ssa_reg_t result)
{
	for (int i = 0; i < nssa; i++) {
		struct ssa_insn *insn = &ssa_insns[i];

		printf("  r%-3d = ", insn->dest);
		switch (insn->type) {
		case SSA_LOAD_LITERAL:
			printf("load %g", insn->load.literal);
			break;
		case SSA_LOAD_VAR:
			printf("load_var %c", insn->load_var.var);
			break;
		case SSA_UNARY_NEGATIVE:
			printf("neg r%d", insn->uneg.src);
			break;
		case SSA_BINARY_OP:
			printf("r%d %c r%d", insn->binop.left,
			       operator_char(insn->binop.op),
			       insn->binop.right);
			break;
		case SSA_UN_INTRIN:
			printf("%s r%d", intrinsic_name(insn->un_intrin.intrin),
			       insn->un_intrin.src);
			break;
		case SSA_BIN_INTRIN:
			printf("%s r%d, r%d", bin_intrinsic_name(insn->bin_intrin.fn),
			       insn->bin_intrin.left, insn->bin_intrin.right);
			break;
		}
		printf("\n");
	}
	printf("  result: r%d\n", result);
}

/* allocate unlimited SSA to 4 registers */
enum ir_reg { REG_A, REG_B, REG_C, REG_D, NUM_REGS };

enum ir_insn_type {
	IR_LOAD_LITERAL,
	IR_LOAD_INPUT,
	IR_BINARY,
	IR_NEGATE,
	IR_UN_INTRIN,
	IR_BIN_INTRIN,
	IR_CHECK_BOUNDS,
	IR_SPILL,
	IR_RESTORE,
};

struct ir_insn {
	enum ir_insn_type type;
	union {
		struct { enum ir_reg dest; double val; } load_lit;
		struct { enum ir_reg dest; int idx; } load_input;
		struct { enum ir_reg dest, left, right; enum operator_type op; } binary;
		struct { enum ir_reg dest, src; } negate;
		struct { enum ir_reg dest, src; enum intrinsic_type fn; } un_intrin;
		struct { enum ir_reg dest, left, right; enum bin_intrinsic_type fn; } bin_intrin;
		struct { enum ir_reg reg; } check_bounds;
		struct { enum ir_reg reg; int slot; } spill;
		struct { enum ir_reg reg; int slot; } restore;
	};
};

/* where an SSA register currently lives */
enum var_state { VAR_UNINITIALIZED, VAR_REGISTER, VAR_SPILLED, VAR_DROPPED };

struct var_loc {
	enum var_state state;
	union {
		enum ir_reg reg;   /* VAR_REGISTER */
		int slot;          /* VAR_SPILLED */
	};
};

#define MAX_IR 1024

static struct ir_insn ir_insns[MAX_IR];
static int nir;

static struct var_loc var_locs[MAX_SSA];   /* per SSA register */
static ssa_reg_t reg_owner[NUM_REGS];      /* SSA reg in each phys reg, -1 = free */
static int last_use[MAX_SSA];              /* last instruction that reads each SSA reg */
static int nspill_slots;                   /* current spill-stack depth */
static int max_spill_slots;                /* spill-area high-water mark */
static int in_use[NUM_REGS];               /* regs pinned for the current insn */
static int bounds_checked[MAX_SSA];        /* SSA regs already bounds-checked */

static void emit_ir(struct ir_insn insn)
{
	if (nir >= MAX_IR) {
		fprintf(stderr, "error: too many IR instructions\n");
		exit(1);
	}
	ir_insns[nir++] = insn;
}

/* record the last instruction index that reads each reg */
static void compute_liveness(ssa_reg_t result)
{
	for (int i = 0; i < nssa; i++)
		last_use[i] = i;

	for (int i = 0; i < nssa; i++) {
		struct ssa_insn *insn = &ssa_insns[i];

		switch (insn->type) {
		case SSA_BINARY_OP:
			last_use[insn->binop.left] = i;
			last_use[insn->binop.right] = i;
			break;
		case SSA_UNARY_NEGATIVE:
			last_use[insn->uneg.src] = i;
			break;
		case SSA_UN_INTRIN:
			last_use[insn->un_intrin.src] = i;
			break;
		case SSA_BIN_INTRIN:
			last_use[insn->bin_intrin.left] = i;
			last_use[insn->bin_intrin.right] = i;
			break;
		case SSA_LOAD_LITERAL:
		case SSA_LOAD_VAR:
			break;
		}
	}

	last_use[result] = nssa;   /* result lives past the end */
}

/* get a register for sr, spilling the value used farthest in the future */
static enum ir_reg alloc_reg(ssa_reg_t sr)
{
	int victim = -1;

	for (enum ir_reg r = REG_A; r < NUM_REGS; r++) {
		if (reg_owner[r] < 0) {
			reg_owner[r] = sr;
			var_locs[sr] = (struct var_loc){ VAR_REGISTER, { .reg = r } };
			// register available, take
			in_use[r] = 1; // pin for current insn
			return r;
		}
		if (in_use[r])
			continue;   /* never spill pinned register */
		if (victim < 0 || last_use[reg_owner[r]] > last_use[reg_owner[victim]])
			victim = r;
	}

	if (in_use[victim]) {
		// should be unreachable if generate_ir logic is correct
		fprintf(stderr, "error: no IR register available to spill; all pinned\n");
		exit(1);
	}

	// spill the non-pinned victim used farthest in the future
	emit_ir((struct ir_insn){
		.type = IR_SPILL,
		.spill = { .reg = victim, .slot = nspill_slots },
	});
	var_locs[reg_owner[victim]] =
		(struct var_loc){ VAR_SPILLED, { .slot = nspill_slots } };
	nspill_slots++;
	if (nspill_slots > max_spill_slots)
		max_spill_slots = nspill_slots;

	reg_owner[victim] = sr;
	var_locs[sr] = (struct var_loc){ VAR_REGISTER, { .reg = victim } };
	in_use[victim] = 1; // pin for current insn
	return victim;
}

/* make sure sr is in a register, restoring from its spill slot if needed */
static enum ir_reg ensure_reg(ssa_reg_t sr)
{
	if (var_locs[sr].state == VAR_REGISTER)
		return var_locs[sr].reg;

	// restore from spill slot
	int slot = var_locs[sr].slot;
	enum ir_reg r = alloc_reg(sr);
	emit_ir((struct ir_insn){
		.type = IR_RESTORE,
		.restore = { .reg = r, .slot = slot },
	});

	nspill_slots--;
	return r;
}

/* drop a source consumed for the last time, freeing its register */
static void drop_if_dead(ssa_reg_t sr, enum ir_reg r, int i)
{
	if (last_use[sr] == i) {
		reg_owner[r] = -1;
		var_locs[sr].state = VAR_DROPPED;
	}
}

/* call at the start of each cycle */
static void reset_pinned_registers(void)
{
	for (enum ir_reg r = REG_A; r < NUM_REGS; r++)
		in_use[r] = 0;
}

/* lower SSA to 4-register IR; returns the IR register holding the result */
static enum ir_reg generate_ir(ssa_reg_t result_var)
{
	compute_liveness(result_var);

	nir = 0;
	nspill_slots = 0;
	max_spill_slots = 0;
	for (enum ir_reg r = REG_A; r < NUM_REGS; r++)
		reg_owner[r] = -1;
	memset(var_locs, 0, sizeof(var_locs));
	memset(bounds_checked, 0, sizeof(bounds_checked));

	for (int i = 0; i < nssa; i++) {
		struct ssa_insn *insn = &ssa_insns[i];
		enum ir_reg dest, left, right, src;

		reset_pinned_registers();

		switch (insn->type) {
		case SSA_LOAD_LITERAL:
			dest = alloc_reg(i);
			emit_ir((struct ir_insn){
				.type = IR_LOAD_LITERAL,
				.load_lit = { dest, insn->load.literal },
			});
			break;

		case SSA_LOAD_VAR:
			dest = alloc_reg(i);
			emit_ir((struct ir_insn){
				.type = IR_LOAD_INPUT,
				.load_input = { dest, insn->load_var.var - 'a' },
			});
			break;

		case SSA_UNARY_NEGATIVE:
			src = ensure_reg(insn->uneg.src);
			drop_if_dead(insn->uneg.src, src, i);
			dest = alloc_reg(i);
			emit_ir((struct ir_insn){
				.type = IR_NEGATE,
				.negate = { dest, src },
			});
			break;

		case SSA_UN_INTRIN:
			src = ensure_reg(insn->un_intrin.src);
			if (insn->un_intrin.intrin == INTRIN_LOAD &&
			    !bounds_checked[insn->un_intrin.src]) {
				/* only bounds check on the first usage of this ssa var */
				emit_ir((struct ir_insn){
					.type = IR_CHECK_BOUNDS,
					.check_bounds = { src },
				});
				bounds_checked[insn->un_intrin.src] = 1;
			}
			drop_if_dead(insn->un_intrin.src, src, i);
			dest = alloc_reg(i);
			emit_ir((struct ir_insn){
				.type = IR_UN_INTRIN,
				.un_intrin = { dest, src, insn->un_intrin.intrin },
			});
			break;

		case SSA_BIN_INTRIN:
			left = ensure_reg(insn->bin_intrin.left);
			right = ensure_reg(insn->bin_intrin.right);
			if (insn->bin_intrin.fn == BININTRIN_STORE &&
			    !bounds_checked[insn->bin_intrin.left]) {
				/* only bounds check on the first usage of this ssa var */
				emit_ir((struct ir_insn){
					.type = IR_CHECK_BOUNDS,
					.check_bounds = { left },
				});
				bounds_checked[insn->bin_intrin.left] = 1;
			}
			drop_if_dead(insn->bin_intrin.left, left, i);
			drop_if_dead(insn->bin_intrin.right, right, i);
			dest = alloc_reg(i);
			emit_ir((struct ir_insn){
				.type = IR_BIN_INTRIN,
				.bin_intrin = { dest, left, right, insn->bin_intrin.fn },
			});
			break;

		case SSA_BINARY_OP:
			left = ensure_reg(insn->binop.left);
			right = ensure_reg(insn->binop.right);
			drop_if_dead(insn->binop.left, left, i);
			drop_if_dead(insn->binop.right, right, i);
			dest = alloc_reg(i);
			/* ^ is not a native IR op; lower it to the pow intrinsic */
			if (insn->binop.op == OP_POW)
				emit_ir((struct ir_insn){
					.type = IR_BIN_INTRIN,
					.bin_intrin = { dest, left, right, BININTRIN_POW },
				});
			else
				emit_ir((struct ir_insn){
					.type = IR_BINARY,
					.binary = { dest, left, right, insn->binop.op },
				});
			break;
		}
	}

	// make sure result is in a register
	reset_pinned_registers();
	enum ir_reg result_reg = ensure_reg(result_var);

	return result_reg;
}

static void print_ir(enum ir_reg result_reg)
{
	const char *name = "ABCD";

	for (int i = 0; i < nir; i++) {
		struct ir_insn *insn = &ir_insns[i];

		switch (insn->type) {
		case IR_LOAD_LITERAL:
			printf("  %c = load %g\n", name[insn->load_lit.dest],
			       insn->load_lit.val);
			break;
		case IR_LOAD_INPUT:
			printf("  %c = load_input %c\n", name[insn->load_input.dest],
			       'a' + insn->load_input.idx);
			break;
		case IR_BINARY:
			printf("  %c = %c %c %c\n", name[insn->binary.dest],
			       name[insn->binary.left],
			       operator_char(insn->binary.op),
			       name[insn->binary.right]);
			break;
		case IR_NEGATE:
			printf("  %c = neg %c\n", name[insn->negate.dest],
			       name[insn->negate.src]);
			break;
		case IR_UN_INTRIN:
			printf("  %c = %s %c\n", name[insn->un_intrin.dest],
			       intrinsic_name(insn->un_intrin.fn),
			       name[insn->un_intrin.src]);
			break;
		case IR_BIN_INTRIN:
			printf("  %c = %s %c %c\n", name[insn->bin_intrin.dest],
			       bin_intrinsic_name(insn->bin_intrin.fn),
			       name[insn->bin_intrin.left],
			       name[insn->bin_intrin.right]);
			break;
		case IR_CHECK_BOUNDS:
			printf("  check_bounds %c\n", name[insn->check_bounds.reg]);
			break;
		case IR_SPILL:
			printf("  spill %c -> [%d]\n", name[insn->spill.reg],
			       insn->spill.slot);
			break;
		case IR_RESTORE:
			printf("  restore [%d] -> %c\n", insn->restore.slot,
			       name[insn->restore.reg]);
			break;
		}
	}
	printf("  result: %c\n", name[result_reg]);
	printf("  (stack slots used: %d)\n", max_spill_slots);
}

/* x86-64 code generation via the chasm assembler */

#define MAX_INSTRUCTIONS 4096

static x64Ins x64_prog[MAX_INSTRUCTIONS];
static size_t n_x64;

/* push an x64 instruction, return its index */
static size_t emit_x64(x64Ins insn)
{
	if (n_x64 >= MAX_INSTRUCTIONS) {
		fprintf(stderr, "error: too many x64 instructions\n");
		exit(1);
	}
	x64_prog[n_x64] = insn;
	return n_x64++;
}

static double inputs[26];                   /* filled by init_vars() */
static char var_order[26];                  /* variable names, in column order */
static int n_var_order;
static double (*calculator_func)(const double *inputs, double *mem);
static uint32_t calculator_func_size;       /* exec mapping size, for cleanup_exec() */

/* IR register -> xmm operand (A,B,C,D -> xmm0,xmm1,xmm2,xmm3) */
static x64Operand xreg(enum ir_reg r)
{
	switch (r) {
	case REG_B: return xmm1;
	case REG_C: return xmm2;
	case REG_D: return xmm3;
	case REG_A:
	default:    return xmm0;
	}
}

/* called from JIT code when a mem[] index is out of bounds */
static void fail_oob(int cause)
{
	fprintf(stderr, "out of bounds memory access: index %d\n", cause);
	exit(1);
}

/* libm function pointer for a unary math intrinsic (sqrt/load handled inline) */
static void *unary_libm(enum intrinsic_type fn)
{
	switch (fn) {
	case INTRIN_SIN: return (void *) sin;
	case INTRIN_COS: return (void *) cos;
	case INTRIN_EXP: return (void *) exp;
	case INTRIN_LOG: return (void *) log;
	default:         return NULL;
	}
}

/*
 * lol cope with syntax
 */
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wmissing-braces"
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#pragma GCC diagnostic ignored "-Wparentheses"
#pragma GCC diagnostic ignored "-Wcast-function-type"

/* save / restore the four IR registers around an external call */
static void emit_call_save(int save)
{
	emit_x64((x64Ins){ MOVSD, m64($rsp, save + 0),  xmm0 });
	emit_x64((x64Ins){ MOVSD, m64($rsp, save + 8),  xmm1 });
	emit_x64((x64Ins){ MOVSD, m64($rsp, save + 16), xmm2 });
	emit_x64((x64Ins){ MOVSD, m64($rsp, save + 24), xmm3 });
}

static void emit_call_restore(int save)
{
	emit_x64((x64Ins){ MOVSD, xmm0, m64($rsp, save + 0) });
	emit_x64((x64Ins){ MOVSD, xmm1, m64($rsp, save + 8) });
	emit_x64((x64Ins){ MOVSD, xmm2, m64($rsp, save + 16) });
	emit_x64((x64Ins){ MOVSD, xmm3, m64($rsp, save + 24) });
}

/* lower the IR to machine code and install it as calculator_func */
static void jit_compile(enum ir_reg result_reg)
{
	int save = max_spill_slots * 8;          /* xmm-save area offset */
	int frame = (save + 32 + 15) & ~15;      /* spill slots + 32 save bytes, 16-aligned */

	n_x64 = 0;

	/* prologue: keep inputs/mem in callee-saved regs (survive libm calls) */
	emit_x64((x64Ins){ PUSH, rbp });
	emit_x64((x64Ins){ MOV, rbp, rsp });
	emit_x64((x64Ins){ PUSH, rbx });
	emit_x64((x64Ins){ PUSH, r12 });
	emit_x64((x64Ins){ SUB, rsp, im32(frame) });
	emit_x64((x64Ins){ MOV, rbx, rdi });     /* inputs */
	emit_x64((x64Ins){ MOV, r12, rsi });     /* mem */

	for (int i = 0; i < nir; i++) {
		struct ir_insn *in = &ir_insns[i];

		switch (in->type) {
		case IR_LOAD_INPUT:
			emit_x64((x64Ins){ MOVSD, xreg(in->load_input.dest),
			                   m64($rbx, in->load_input.idx * 8) });
			break;

		case IR_LOAD_LITERAL: {
			union { double d; int64_t i; } u;
			u.d = in->load_lit.val;
			emit_x64((x64Ins){ MOV, rax, im64(u.i) });
			emit_x64((x64Ins){ MOVQ, xreg(in->load_lit.dest), rax });
			break;
		}

		case IR_BINARY: {
			x64Op op = ADDSD;
			switch (in->binary.op) {
			case OP_ADD: op = ADDSD; break;
			case OP_SUB: op = SUBSD; break;
			case OP_MUL: op = MULSD; break;
			case OP_DIV: op = DIVSD; break;
			case OP_POW: op = ADDSD; break;   /* unreachable: pow is an intrinsic */
			}
			emit_x64((x64Ins){ MOVSD, xmm5, xreg(in->binary.left) });
			emit_x64((x64Ins){ op, xmm5, xreg(in->binary.right) });
			emit_x64((x64Ins){ MOVSD, xreg(in->binary.dest), xmm5 });
			break;
		}

		case IR_NEGATE:
			emit_x64((x64Ins){ XORPS, xmm4, xmm4 });
			emit_x64((x64Ins){ SUBSD, xmm4, xreg(in->negate.src) });
			emit_x64((x64Ins){ MOVSD, xreg(in->negate.dest), xmm4 });
			break;

		case IR_UN_INTRIN:
			if (in->un_intrin.fn == INTRIN_SQRT) {
				emit_x64((x64Ins){ SQRTSD, xreg(in->un_intrin.dest),
				                   xreg(in->un_intrin.src) });
			} else if (in->un_intrin.fn == INTRIN_LOAD) {
				emit_x64((x64Ins){ CVTTSD2SI, rax, xreg(in->un_intrin.src) });
				emit_x64((x64Ins){ MOVSD, xreg(in->un_intrin.dest),
				                   m64($r12, 0, $rax, 8) });
			} else {
				emit_call_save(save);
				emit_x64((x64Ins){ MOVSD, xmm0,
				                   m64($rsp, save + in->un_intrin.src * 8) });
				emit_x64((x64Ins){ MOV, rax, imptr(unary_libm(in->un_intrin.fn)) });
				emit_x64((x64Ins){ CALL, rax });
				emit_x64((x64Ins){ MOVSD, xmm5, xmm0 });
				emit_call_restore(save);
				emit_x64((x64Ins){ MOVSD, xreg(in->un_intrin.dest), xmm5 });
			}
			break;

		case IR_BIN_INTRIN:
			if (in->bin_intrin.fn == BININTRIN_MAX ||
			    in->bin_intrin.fn == BININTRIN_MIN) {
				x64Op op = in->bin_intrin.fn == BININTRIN_MAX ? MAXSD : MINSD;
				emit_x64((x64Ins){ MOVSD, xmm5, xreg(in->bin_intrin.left) });
				emit_x64((x64Ins){ op, xmm5, xreg(in->bin_intrin.right) });
				emit_x64((x64Ins){ MOVSD, xreg(in->bin_intrin.dest), xmm5 });
			} else if (in->bin_intrin.fn == BININTRIN_STORE) {
				emit_x64((x64Ins){ CVTTSD2SI, rax, xreg(in->bin_intrin.left) });
				emit_x64((x64Ins){ MOVSD, m64($r12, 0, $rax, 8),
				                   xreg(in->bin_intrin.right) });
				if (in->bin_intrin.dest != in->bin_intrin.right)
					emit_x64((x64Ins){ MOVSD, xreg(in->bin_intrin.dest),
					                   xreg(in->bin_intrin.right) });
			} else {   /* BININTRIN_POW */
				emit_call_save(save);
				emit_x64((x64Ins){ MOVSD, xmm0,
				                   m64($rsp, save + in->bin_intrin.left * 8) });
				emit_x64((x64Ins){ MOVSD, xmm1,
				                   m64($rsp, save + in->bin_intrin.right * 8) });
				emit_x64((x64Ins){ MOV, rax, imptr((void *) pow) });
				emit_x64((x64Ins){ CALL, rax });
				emit_x64((x64Ins){ MOVSD, xmm5, xmm0 });
				emit_call_restore(save);
				emit_x64((x64Ins){ MOVSD, xreg(in->bin_intrin.dest), xmm5 });
			}
			break;

		case IR_CHECK_BOUNDS:
			/* one unsigned compare rejects both <0 and >=MEM_SIZE */
			emit_x64((x64Ins){ CVTTSD2SI, rax, xreg(in->check_bounds.reg) });
			emit_x64((x64Ins){ CMP, rax, im32(MEM_SIZE) });
			emit_x64((x64Ins){ JB, rel(4) });           /* in bounds: skip fail */
			emit_x64((x64Ins){ MOV, edi, eax });        /* cause = bad index */
			emit_x64((x64Ins){ MOV, rax, imptr((void *) fail_oob) });
			emit_x64((x64Ins){ CALL, rax });
			break;

		case IR_SPILL:
			emit_x64((x64Ins){ MOVSD, m64($rsp, in->spill.slot * 8),
			                   xreg(in->spill.reg) });
			break;

		case IR_RESTORE:
			emit_x64((x64Ins){ MOVSD, xreg(in->restore.reg),
			                   m64($rsp, in->restore.slot * 8) });
			break;
		}
	}

	/* epilogue: result must be in xmm0 */
	if (result_reg != REG_A)
		emit_x64((x64Ins){ MOVSD, xmm0, xreg(result_reg) });
	emit_x64((x64Ins){ ADD, rsp, im32(frame) });
	emit_x64((x64Ins){ POP, r12 });
	emit_x64((x64Ins){ POP, rbx });
	emit_x64((x64Ins){ POP, rbp });
	emit_x64((x64Ins){ RET });

	uint32_t len = 0;
	uint8_t *bytes = x64as(x64_prog, (uint32_t) n_x64, &len);
	if (!bytes) {
		fprintf(stderr, "jit asm error: %s\n", x64error(NULL));
		exit(1);
	}
	calculator_func = (double (*)(const double *, double *)) x64exec(bytes, len);
	calculator_func_size = len;
	free(bytes);   /* x64exec copies into its own executable mapping */
}

#pragma GCC diagnostic pop

/* input-driven runtime */

/* read the variable-name line, e.g. "b a e" -> var_order */
static void read_var_line(void)
{
	char line[256];

	printf("Enter list of input variables:\n");
	if (!fgets(line, sizeof line, stdin)) {
		fprintf(stderr, "error: missing variable list\n");
		exit(1);
	}

	n_var_order = 0;
	for (int i = 0; line[i] && line[i] != '\n'; i++) {
		if (line[i] == ' ')
			continue;
		if (line[i] < 'a' || line[i] > 'z') {
			fprintf(stderr, "error: variable list must be space-separated a-z letters\n");
			exit(1);
		}
		/* a variable is one letter; the next char must be a space or end */
		if (line[i + 1] >= 'a' && line[i + 1] <= 'z') {
			fprintf(stderr, "error: variables must be single letters separated by spaces\n");
			exit(1);
		}
		if (n_var_order >= (int) sizeof var_order) {
			fprintf(stderr, "error: too many variables (max %d)\n",
				(int) sizeof var_order);
			exit(1);
		}
		var_order[n_var_order++] = line[i];
	}

	printf("Enter values for variables, one set per line\n\n");
}

/* read one value line into inputs[]. return 0 if nothing */
static int init_vars(void)
{
	char line[1024];
	char *p, *end;

	memset(inputs, 0, sizeof(inputs));

	if (!fgets(line, sizeof line, stdin))
		return 0;

	/* a blank (whitespace-only) line ends input */
	p = line;
	while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n')
		p++;
	if (*p == '\0')
		return 0;

	/* anything that isn't exactly n_var_order numbers also ends input */
	p = line;
	for (int k = 0; k < n_var_order; k++) {
		double v = strtod(p, &end);
		if (end == p)
			return 0;
		inputs[var_order[k] - 'a'] = v;
		p = end;
	}
	while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n')
		p++;
	if (*p != '\0')
		return 0;

	return 1;
}

static void calculate_queries(void)
{
	double mem[MEM_SIZE];

	memset(mem, 0, sizeof mem);

	read_var_line();
	while (init_vars()) {
		double result = calculator_func(inputs, mem);
		printf("%.17g\n", result);
	}
}

/* release the JIT-compiled function's executable mapping */
static void cleanup_exec(void)
{
	if (calculator_func) {
		x64exec_free((void *) calculator_func, calculator_func_size);
		calculator_func = NULL;
	}
}

int main(void)
{
	char line[4096];

	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	printf("Enter expression:\n");
	if (!fgets(line, sizeof(line), stdin)) {
		fprintf(stderr, "error: no input\n");
		return 1;
	}

	if (tokenize(line) < 0)
		return 1;

	ssa_reg_t result_var = parse();
	if (result_var < 0)
		return 1;

	enum ir_reg result_reg = generate_ir(result_var);

	if (getenv("JIT_DEBUG")) {
		print_ssa(result_var);
		printf("\n");
		print_ir(result_reg);
		printf("\n");
	}

	jit_compile(result_reg);
	calculate_queries();
	cleanup_exec();

	return 0;
}
