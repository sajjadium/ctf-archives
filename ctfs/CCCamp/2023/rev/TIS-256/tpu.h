#pragma once

#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

#define TPU_MAP_BUCKETS 64
#define TPU_MAX_INST 256

/* enum order is important ! */

enum tpu_status {
	STATUS_IDLE, STATUS_RUN, STATUS_READ, STATUS_WRITE
};

enum tpu_inst_type {
	INST_NOP, INST_MOV, INST_SWP, INST_SAV, INST_ADD,
	INST_SUB, INST_NEG, INST_XOR, INST_AND, INST_JMP,
	INST_JEQ, INST_JNE, INST_JRO, INST_SHL, INST_SHR
};

enum tpu_inst_op_type {
	OP_ACC, OP_NIL, OP_LEFT, OP_RIGHT, OP_UP, OP_DOWN,
	OP_ANY, OP_LAST, OP_LIT, OP_LABEL
};

enum tpu_port_dir {
	DIR_LEFT, DIR_RIGHT, DIR_UP, DIR_DOWN
};

enum tpu_port_type {
	PORT_IN = 0b01, PORT_OUT = 0b10, PORT_BIDI = 0b11
};

union tpu_inst_op_val {
	uint8_t lit;
	char *label;
};

struct tpu_inst_op {
	enum tpu_inst_op_type type;
	union tpu_inst_op_val val;
};

struct tpu_inst {
	enum tpu_inst_type type;
	struct tpu_inst_op ops[2];
	unsigned opcnt;
};

struct tpu_port {
	struct tpu *dst_tpu;
	enum tpu_port_type type;
	struct tpu_port *dst_port;
	bool clr_post_run;
	bool reading, writing;
	bool attached;
	bool could_read;
	bool could_write;
	bool empty;
	int in, out, out_pending;
};

struct tpu {
	struct tis *tis;

	enum tpu_status status;
	int x, y;

	struct tpu_port ports[4];
	int io_port;
	int last;

	size_t steps;
	size_t idle_steps;

	void *user;

	uint8_t acc, bak;
	uint8_t pc;
	char *labels[TPU_MAX_INST];
	int jmpdst[TPU_MAX_INST];
	struct tpu_inst insts[TPU_MAX_INST];
	size_t inst_cnt;
};

struct tpu_map_link {
	int x, y;
	struct tpu *tpu;
	struct tpu_map_link *next;
};

struct tpu_map {
	struct tpu_map_link *buckets[TPU_MAP_BUCKETS];
};

struct tpu_vec {
	struct tpu *tpus;
	size_t cnt, cap;
};

struct tis {
	size_t steps;
	bool alive, idle, prev_idle;
	struct tpu_vec tpu_vec;
	struct tpu_map tpu_map;
	FILE *stdin;
	struct tpu_port stdin_port;
	FILE *stdout;
	struct tpu_port stdout_port;
};

void tpu_port_init(struct tpu_port *port);
void tpu_port_deinit(struct tpu_port *port);

void tpu_init(struct tpu *tpu);
void tpu_deinit(struct tpu *tpu);
bool tpu_label_add(struct tpu *tpu, const char *name, size_t pc);
size_t tpu_label_get(struct tpu *tpu, const char *name);
void tpu_init_ports(struct tpu *tpu, struct tpu_map *map);
void tpu_attach_ports(struct tpu *tpu);
bool tpu_set_inst(struct tpu *tpu, uint8_t pc, enum tpu_inst_type inst,
	unsigned opcnt, struct tpu_inst_op op1, struct tpu_inst_op op2);
bool tpu_add_inst(struct tpu *tpu, enum tpu_inst_type inst,
	unsigned opcnt, struct tpu_inst_op op1, struct tpu_inst_op op2);
void tpu_clear_ports(struct tpu *tpu);
enum tpu_status tpu_step(struct tpu *tpu);

void tpu_vec_init(struct tpu_vec *vec);
void tpu_vec_deinit(struct tpu_vec *vec);

void tpu_map_init(struct tpu_map *map);
void tpu_map_deinit(struct tpu_map *map);
bool tpu_map_add(struct tpu_map *map, struct tpu *tpu);
struct tpu *tpu_map_get(struct tpu_map *map, int x, int y);

void tis_init(struct tis *tis, FILE *tis_stdin, FILE *tis_stdout);
void tis_deinit(struct tis *tis);
bool tis_step(struct tis *tis);
struct tpu *tis_add_tpu(struct tis *tis);

extern const char *dir_reprs[];
extern const char *status_reprs[];
extern const char *inst_reprs[];
extern const char *op_reprs[];
