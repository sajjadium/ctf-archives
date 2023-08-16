#include "tpu.h"
#include "util.h"

#include <ctype.h>
#include <stdio.h>
#include <stdbool.h>
#include <stddef.h>
#include <string.h>

const char *dir_reprs[] = {
	"LEFT", "RIGHT", "UP", "DOWN"
};

const char *status_reprs[] = {
	"IDLE", "RUN", "READ", "WRITE"
};

const char *inst_reprs[] = {
	"NOP", "MOV", "SWP", "SAV", "ADD",
	"SUB", "NEG", "XOR", "AND", "JMP",
	"JEQ", "JNE", "JRO", "SHL", "SHR"
};

const char *op_reprs[] = {
	"ACC", "NIL", "LEFT", "RIGHT", "UP", "DOWN",
	"ANY", "LAST", "LIT", "<NAME>"
};

static bool
op_is_dir(enum tpu_inst_op_type op)
{
	return op >= OP_LEFT && op <= OP_DOWN;
}

static enum tpu_port_dir
op_to_dir(enum tpu_inst_op_type op)
{
	return op - OP_LEFT;
}

static enum tpu_port_dir
opposite_dir(enum tpu_port_dir dir)
{
	switch (dir) {
	case DIR_UP:
		return DIR_DOWN;
	case DIR_DOWN:
		return DIR_UP;
	case DIR_LEFT:
		return DIR_RIGHT;
	case DIR_RIGHT:
		return DIR_LEFT;
	}
}

void
tpu_port_init(struct tpu_port *port)
{
	port->attached = false;
	port->dst_port = NULL;
	port->dst_tpu = NULL;
	port->type = 0;
	port->clr_post_run = false;
	port->reading = false;
	port->writing = false;
	port->could_read = false;
	port->could_write = false;
	port->empty = true;
	port->in = -1;
	port->out = -1;
	port->out_pending = -1;
}

void
tpu_port_deinit(struct tpu_port *port)
{
	/* empty */
}

void
tpu_init(struct tpu *tpu)
{
	size_t i;

	tpu->status = STATUS_IDLE;

	tpu->x = 0;
	tpu->y = 0;

	tpu->steps = 0;
	tpu->idle_steps = 0;

	tpu->user = NULL;

	tpu->pc = 0;
	tpu->acc = 0;
	tpu->bak = 0;
	tpu->inst_cnt = 0;
	memset(tpu->labels, 0, sizeof(char *) * TPU_MAX_INST);
	memset(tpu->jmpdst, 0xff, sizeof(int) * TPU_MAX_INST);

	tpu->last = -1;
	tpu->io_port = -1;
	for (i = 0; i < 4; i++)
		tpu_port_init(&tpu->ports[i]);
}

void
tpu_deinit(struct tpu *tpu)
{
	int i;

	for (i = 0; i < tpu->inst_cnt; i++) {
		if (tpu->insts[i].opcnt >= 1
				&& tpu->insts[i].ops[0].type == OP_LABEL)
			free(tpu->insts[i].ops[0].val.label);
	}
	for (i = 0; i < TPU_MAX_INST; i++)
		free(tpu->labels[i]);
}

bool
tpu_label_add(struct tpu *tpu, const char *name, size_t pc)
{
	if (tpu->labels[pc]) return false;
	if (tpu_label_get(tpu, name) != TPU_MAX_INST) return false;

	tpu->labels[pc] = strdup(name);
	if (!tpu->labels[pc]) die("strdup");

	return true;
}

size_t
tpu_label_get(struct tpu *tpu, const char *name)
{
	size_t i;

	for (i = 0; i < TPU_MAX_INST; i++) {
		if (tpu->labels[i] && !strcasecmp(tpu->labels[i], name))
			return i;
	}

	return TPU_MAX_INST;
}

void
tpu_init_ports(struct tpu *tpu, struct tpu_map *map)
{
	const int dx[4] = { -1, 1, 0, 0 };
	const int dy[4] = { 0, 0, -1, 1 };
	enum tpu_port_dir dir, odir;
	enum tpu_inst_op_type optype;
	struct tpu *neighbor;
	int x, y, i, k, l;

	for (i = 0; i < tpu->inst_cnt; i++) {
		for (k = 0; k < tpu->insts[i].opcnt; k++) {
			optype = tpu->insts[i].ops[k].type;
			if (op_is_dir(optype)) {
				dir = op_to_dir(tpu->insts[i].ops[k].type);
				if (k == 0)
					tpu->ports[dir].could_read = true;
				else
					tpu->ports[dir].could_write = true;
			} else if (optype == OP_ANY) {
				for (l = 0; l < 4; l++) {
					if (k == 0)
						tpu->ports[l].could_read = true;
					else
						tpu->ports[l].could_write = true;
				}
			} else if (optype == OP_LAST && k == 1) {
				for (l = 0; l < 4; l++) {
					if (tpu->ports[l].could_read)
						tpu->ports[l].could_write = true;
				}
			}
		}
	}

	for (i = 0; i < 4; i++) {
		x = tpu->x + dx[i];
		y = tpu->y + dy[i];
		neighbor = tpu_map_get(map, x, y);
		tpu->ports[i].dst_tpu = neighbor;
		tpu->ports[i].type = tpu->ports[i].could_read * PORT_IN
			| tpu->ports[i].could_write * PORT_OUT;
		if (neighbor && tpu->ports[i].type != 0) {
			odir = opposite_dir((enum tpu_port_dir) i);
			tpu->ports[i].dst_port = &neighbor->ports[odir];
		}
	}
}

void
tpu_attach_ports(struct tpu *tpu)
{
	struct tpu *neighbor;
	enum tpu_port_dir i, o;

	for (i = 0; i < 4; i++) {
		neighbor = tpu->ports[i].dst_tpu;
		if (!neighbor) continue;
		o = opposite_dir(i);
		if (tpu->ports[i].type & PORT_IN && neighbor->ports[o].type & PORT_OUT)
			tpu->ports[i].attached = true;
		if (tpu->ports[i].type & PORT_OUT && neighbor->ports[o].type & PORT_IN)
			tpu->ports[i].attached = true;
	}
}

static void
tpu_update_ports(struct tpu *tpu)
{
	struct tpu_port *port;
	int i;

	for (i = 0; i < 4; i++) {
		port = &tpu->ports[i];
		if (!port->attached) continue;
		if (port->out >= 0 && port->dst_port->in < 0) {
			port->dst_port->reading = false;
			port->dst_port->in = port->out;
			port->writing = false;
			port->out = -1;
		}
		if (port->dst_port->out >= 0 && port->in < 0) {
			port->reading = false;
			port->in = port->dst_port->out;
			port->dst_port->writing = false;
			port->dst_port->out = -1;
		}
		if (tpu->status == STATUS_RUN && port->clr_post_run) {
			port->in = -1;
			port->clr_post_run = false;
		}
		port->empty = port->in < 0;
	}
}

bool
tpu_set_inst(struct tpu *tpu, uint8_t pc, enum tpu_inst_type inst_type,
	unsigned opcnt, struct tpu_inst_op op1, struct tpu_inst_op op2)
{
	struct tpu_inst *inst;

	inst = &tpu->insts[pc];
	inst->type = inst_type;
	inst->opcnt = opcnt;
	inst->ops[0] = op1;
	inst->ops[1] = op2;

	switch (inst->type) {
	case INST_NOP: case INST_SAV:
	case INST_SWP: case INST_NEG:
		if (inst->opcnt != 0) return false;
		break;
	case INST_ADD: case INST_SUB: case INST_XOR:
	case INST_AND: case INST_SHL: case INST_SHR:
		if (inst->opcnt != 1) return false;
		if (inst->ops[0].type == OP_LABEL) return false;
		break;
	case INST_JRO:
		if (inst->opcnt != 1) return false;
		if (inst->ops[0].type != OP_LIT) return false;
		break;
	case INST_JMP:
		if (inst->opcnt != 1) return false;
		if (inst->ops[0].type != OP_LABEL) return false;
		break;
	case INST_JEQ: case INST_JNE:
		if (inst->opcnt != 2) return false;
		if (inst->ops[0].type == OP_LABEL) return false;
		if (inst->ops[1].type != OP_LABEL) return false;
		break;
	case INST_MOV:
		if (inst->opcnt != 2) return false;
		if (inst->ops[0].type == OP_LABEL) return false;
		if (inst->ops[1].type == OP_LABEL) return false;
		if (inst->ops[1].type == OP_LIT) return false;
		break;
	}

	return true;
}

bool
tpu_add_inst(struct tpu *tpu, enum tpu_inst_type inst_type,
	unsigned opcnt, struct tpu_inst_op op1, struct tpu_inst_op op2)
{
	if (tpu->inst_cnt >= TPU_MAX_INST)
		die("tpu_add_inst: tpu X%i Y%i, >= max %i instructions",
			tpu->x, tpu->y, TPU_MAX_INST);
	return tpu_set_inst(tpu, (uint8_t) tpu->inst_cnt++,
		inst_type, opcnt, op1, op2);
}

static int
tpu_port_read(struct tpu *tpu, enum tpu_port_dir dir)
{
	struct tpu_port *port;

	port = &tpu->ports[dir];
	if (port->attached && tpu->tis->stdin
			&& port->dst_port == &tpu->tis->stdin_port && port->in < 0) {
		port->in = getc(tpu->tis->stdin);
		port->in = port->in == EOF ? -1 : (uint8_t) port->in;
	}
	if (port->in < 0) {
		port->reading = true;
		return -1;
	}
	port->clr_post_run = true;
	return port->in;
}

static bool
tpu_port_write(struct tpu *tpu, enum tpu_port_dir dir, uint8_t lit)
{
	struct tpu_port *port;

	port = &tpu->ports[dir];
	if (port->attached && port->dst_port == &tpu->tis->stdout_port) {
		if (tpu->tis->stdout) putc(lit, tpu->tis->stdout);
		return true;
	}
	if (!port->attached || !port->dst_port->empty) {
		port->out_pending = lit;
		port->writing = true;
		return false;
	}
	port->out = lit;
	port->out_pending = -1;
	return true;
}

static void
tpu_jmp_label(struct tpu *tpu, const char *label)
{
	size_t pc;

	if (tpu->jmpdst[tpu->pc] >= 0) {
		tpu->pc = (uint8_t) tpu->jmpdst[tpu->pc];
	} else {
		pc = tpu_label_get(tpu, label);
		if (pc >= TPU_MAX_INST) abort();
		tpu->jmpdst[tpu->pc] = (uint8_t) pc;
		tpu->pc = (uint8_t) pc;
	}
}

static int
tpu_exec_get(struct tpu *tpu, struct tpu_inst_op *op)
{
	int i, v;

	switch (op->type) {
	case OP_ACC:
		return tpu->acc;
	case OP_NIL:
		return -1;
	case OP_LEFT: case OP_RIGHT: case OP_UP: case OP_DOWN:
		return tpu_port_read(tpu, op_to_dir(op->type));
	case OP_ANY:
		for (i = 0; i < 4; i++) {
			v = tpu_port_read(tpu, (enum tpu_port_dir) i);
			if (v >= 0) {
				tpu->last = i;
				return (uint8_t) v;
			}
		}
		return -1;
	case OP_LAST:
		if (tpu->last < 0) return 0;
		return tpu_port_read(tpu, (enum tpu_port_dir) tpu->last);
	case OP_LIT:
		return op->val.lit;
	case OP_LABEL:
		abort();
	}
}

static bool
tpu_exec_put(struct tpu *tpu, struct tpu_inst_op *op, uint8_t lit)
{
	int i;

	switch (op->type) {
	case OP_ACC:
		tpu->acc = lit;
		return true;
	case OP_NIL:
		return true;
	case OP_LEFT: case OP_RIGHT: case OP_UP: case OP_DOWN:
		return tpu_port_write(tpu, op_to_dir(op->type), lit);
	case OP_ANY:
		for (i = 0; i < 4; i++) {
			if (tpu_port_write(tpu, (enum tpu_port_dir) i, lit)) {
				tpu->last = i;
				return true;
			}
		}
		return false;
	case OP_LAST:
		if (tpu->last < 0) return false;
		return tpu_port_write(tpu, (enum tpu_port_dir) tpu->last, lit);
	case OP_LABEL:
	case OP_LIT:
		abort();
	}
}

static enum tpu_status
tpu_exec_mov(struct tpu *tpu, struct tpu_inst *inst)
{
	int lit;

	if (inst->type != INST_MOV) abort();

	lit = tpu_exec_get(tpu, &inst->ops[0]);
	if (lit < 0) return STATUS_READ;

	if (!tpu_exec_put(tpu, &inst->ops[1], (uint8_t) lit))
		return STATUS_WRITE;

	return STATUS_RUN;
}

static enum tpu_status
tpu_exec(struct tpu *tpu, struct tpu_inst *inst)
{
	enum tpu_status status;
	uint8_t lit;
	int val;

	switch (inst->type) {
	case INST_NOP:
		tpu->pc += 1;
		return STATUS_RUN;
	case INST_MOV:
		status = tpu_exec_mov(tpu, inst);
		if (status == STATUS_RUN)
			tpu->pc += 1;
		return status;
	case INST_SWP:
		lit = tpu->acc;
		tpu->acc = tpu->bak;
		tpu->bak = lit;
		tpu->pc += 1;
		return STATUS_RUN;
	case INST_SAV:
		tpu->bak = tpu->acc;
		tpu->pc += 1;
		return STATUS_RUN;
	case INST_ADD:
		val = tpu_exec_get(tpu, &inst->ops[0]);
		if (val < 0) return STATUS_READ;
		tpu->acc += (uint8_t) val;
		tpu->pc += 1;
		return STATUS_RUN;
	case INST_SUB:
		val = tpu_exec_get(tpu, &inst->ops[0]);
		if (val < 0) return STATUS_READ;
		tpu->acc -= (uint8_t) val;
		tpu->pc += 1;
		return STATUS_RUN;
	case INST_NEG:
		tpu->acc = -tpu->acc;
		tpu->pc += 1;
		return STATUS_RUN;
	case INST_XOR:
		val = tpu_exec_get(tpu, &inst->ops[0]);
		if (val < 0) return STATUS_READ;
		tpu->acc ^= (uint8_t) val;
		tpu->pc += 1;
		return STATUS_RUN;
	case INST_AND:
		val = tpu_exec_get(tpu, &inst->ops[0]);
		if (val < 0) return STATUS_READ;
		tpu->acc &= (uint8_t) val;
		tpu->pc += 1;
		return STATUS_RUN;
	case INST_JMP:
		tpu_jmp_label(tpu, inst->ops[0].val.label);
		return STATUS_RUN;
	case INST_JEQ:
		val = tpu_exec_get(tpu, &inst->ops[0]);
		if (val < 0) return STATUS_READ;
		if (tpu->acc == val)
			tpu_jmp_label(tpu, inst->ops[1].val.label);
		else
			tpu->pc += 1;
		return STATUS_RUN;
	case INST_JNE:
		val = tpu_exec_get(tpu, &inst->ops[0]);
		if (val < 0) return STATUS_READ;
		if (tpu->acc != val)
			tpu_jmp_label(tpu, inst->ops[1].val.label);
		else
			tpu->pc += 1;
		return STATUS_RUN;
	case INST_JRO:
		tpu->pc += inst->ops[0].val.lit;
		if (tpu->pc >= tpu->inst_cnt) tpu->pc = 0;
		return STATUS_RUN;
	case INST_SHL:
		val = tpu_exec_get(tpu, &inst->ops[0]);
		if (val < 0) abort();
		tpu->acc <<= val;
		tpu->pc += 1;
		return STATUS_RUN;
	case INST_SHR:
		val = tpu_exec_get(tpu, &inst->ops[0]);
		if (val < 0) abort();
		tpu->acc >>= val;
		tpu->pc += 1;
		return STATUS_RUN;
	}
}

enum tpu_status
tpu_step(struct tpu *tpu)
{
	if (tpu->pc < tpu->inst_cnt) {
		tpu->status = tpu_exec(tpu, &tpu->insts[tpu->pc]);
		if (tpu->pc >= tpu->inst_cnt) tpu->pc = 0;
	} else {
		tpu->status = STATUS_IDLE;
	}

	tpu->steps += 1;
	if (tpu->status != STATUS_RUN)
		tpu->idle_steps += 1;

	return tpu->status;
}

void
tpu_vec_init(struct tpu_vec *vec)
{
	vec->cnt = 0;
	vec->cap = 256;
	vec->tpus = malloc(vec->cap * sizeof(struct tpu));
	if (!vec->tpus) die("malloc:");
}

void
tpu_vec_deinit(struct tpu_vec *vec)
{
	struct tpu *tpu;
	size_t i;

	for (tpu = vec->tpus, i = 0; i < vec->cnt; i++, tpu++)
		tpu_deinit(tpu);
	free(vec->tpus);
}

void
tpu_map_init(struct tpu_map *map)
{
	memset(map->buckets, 0, sizeof(void *) * TPU_MAP_BUCKETS);
}

void
tpu_map_deinit(struct tpu_map *map)
{
	struct tpu_map_link *link, *next;
	size_t i;

	for (i = 0; i < TPU_MAP_BUCKETS; i++) {
		link = map->buckets[i];
		while (link) {
			next = link->next;
			free(link);
			link = next;
		}
	}
}

static struct tpu_map_link **
tpu_map_link_pos(struct tpu_map *map, int x, int y)
{
	struct tpu_map_link **link;
	size_t i;

	i = (size_t) (x + y) % TPU_MAP_BUCKETS;
	link = &map->buckets[i];
	while (*link && !((*link)->x == x && (*link)->y == y))
		link = &(*link)->next;

	return link;
}

bool
tpu_map_add(struct tpu_map *map, struct tpu *tpu)
{
	struct tpu_map_link **pos, *link;

	pos = tpu_map_link_pos(map, tpu->x, tpu->y);
	if (*pos) return false;
	*pos = link = malloc(sizeof(struct tpu_map_link));
	if (!link) die("malloc:");
	link->tpu = tpu;
	link->x = tpu->x;
	link->y = tpu->y;
	link->next = NULL;
	return true;
}

struct tpu *
tpu_map_get(struct tpu_map *map, int x, int y)
{
	struct tpu_map_link **link;

	link = tpu_map_link_pos(map, x, y);
	if (!*link) return NULL;

	return (*link)->tpu;
}

void
tis_init(struct tis *tis, FILE *tis_stdin, FILE *tis_stdout)
{
	tis->steps = 0;
	tis->alive = true;
	tis->idle = tis->prev_idle = false;
	tpu_vec_init(&tis->tpu_vec);
	tpu_map_init(&tis->tpu_map);
	tis->stdin = tis_stdin;
	tpu_port_init(&tis->stdin_port);
	tis->stdin_port.type = PORT_OUT;
	tis->stdout = tis_stdout;
	tpu_port_init(&tis->stdout_port);
	tis->stdout_port.type = PORT_IN;
}

void
tis_deinit(struct tis *tis)
{
	tpu_vec_deinit(&tis->tpu_vec);
	tpu_map_deinit(&tis->tpu_map);
	if (tis->stdin) fclose(tis->stdin);
	tpu_port_deinit(&tis->stdin_port);
	if (tis->stdout) fclose(tis->stdout);
	tpu_port_deinit(&tis->stdout_port);
}

bool
tis_step(struct tis *tis)
{
	struct tpu *tpu;
	bool running;
	size_t i;

	running = false;
	for (tpu = tis->tpu_vec.tpus, i = 0; i < tis->tpu_vec.cnt; i++, tpu++)
		running |= (tpu_step(tpu) == STATUS_RUN);

	for (tpu = tis->tpu_vec.tpus, i = 0; i < tis->tpu_vec.cnt; i++, tpu++)
		tpu_update_ports(tpu);

	tis->prev_idle = tis->idle;
	tis->idle = !running;

	tis->alive = !tis->idle || !tis->prev_idle
		|| tis->stdin_port.reading && !feof(tis->stdin);

	tis->steps++;

	return tis->alive;
}

struct tpu *
tis_add_tpu(struct tis *tis)
{
	struct tpu_port *port;
	struct tpu_vec *vec;
	struct tpu_map_link *link;
	struct tpu *tpu;
	void *old_arena;
	size_t i, k;
	ssize_t off;

	vec = &tis->tpu_vec;
	if (vec->cnt >= vec->cap) {
		vec->cap *= 2;
		old_arena = vec->tpus;
		vec->tpus = realloc(vec->tpus, vec->cap * sizeof(struct tpu));
		if (!vec->tpus) die("realloc:");
		/* AAAAH, dont looook >.< */
		off = (void *) vec->tpus - old_arena;
		for (tpu = vec->tpus, i = 0; i < vec->cnt; i++, tpu++) {
			for (port = tpu->ports, k = 0; k < 4; k++, port++) {
				if (port->dst_tpu)
					port->dst_tpu = (void *)port->dst_tpu + off;
				if (port->dst_port)
					port->dst_port = (void *)port->dst_port + off;
			}
		}
		for (i = 0; i < TPU_MAP_BUCKETS; i++) {
			link = tis->tpu_map.buckets[i];
			for (; link; link = link->next)
				link->tpu = (void *)link->tpu + off;
		}
	}

	return &vec->tpus[vec->cnt++];
}
