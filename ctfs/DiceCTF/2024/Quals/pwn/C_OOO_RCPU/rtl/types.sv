`ifndef TYPES_SV
`define TYPES_SV

`define OPC(INSN)    INSN[6:0]
`define RD(INSN)     INSN[11:7]
`define FUNCT3(INSN) INSN[14:12]
`define RS1(INSN)    INSN[19:15]
`define RS2(INSN)    INSN[24:20]
`define FUNCT7(INSN) INSN[31:25]

`define INSTR(__name, __opc, __enc, __unit) `define OPC_``__name __opc
`include "ops.sv"
`undef INSTR

`define PRIV_ROUTINE_START 16384

typedef enum logic [2:0] {
        R_FORMAT, I_FORMAT, S_FORMAT, B_FORMAT, U_FORMAT, J_FORMAT
} e_instruction_format;
`define INSN_FMT_CNT 6

typedef enum logic [2:0]{
    BU, ALU, LSU, IOU, PU
} e_functional_unit;
`define FU_CNT 5

typedef struct {
    e_instruction_format encoding;
    bit [31:0] insn;
} op_t;

function bit has_rs1(e_instruction_format format);
	return format == R_FORMAT || format == I_FORMAT || format == S_FORMAT || format == B_FORMAT;
endfunction

function bit has_rs2(e_instruction_format format);
	return format == R_FORMAT || format == S_FORMAT || format == B_FORMAT;
endfunction

function bit has_rd(e_instruction_format format);
	return format == R_FORMAT || format == I_FORMAT || format == J_FORMAT || format == U_FORMAT;
endfunction

function bit has_imm(e_instruction_format format);
	return format == I_FORMAT || format == S_FORMAT || format == B_FORMAT
			|| format == J_FORMAT || format == U_FORMAT;
endfunction

function logic [31:0] decode_imm(op_t op);
    case (op.encoding)
        I_FORMAT : return { 20'b0, op.insn[31:20] };
        S_FORMAT : return { 20'b0, op.insn[31:25] , op.insn[11:7] };
        B_FORMAT : return $signed({ op.insn[31] , op.insn[7] , op.insn[30:25] , op.insn[11:8], 1'b0 });
        U_FORMAT : return { op.insn[31:12], 12'b0 };
        J_FORMAT : return { 12'b0, op.insn[31], op.insn[19:12], op.insn[20], op.insn[30:21], 1'b0 };
        default  : return 'X;
    endcase
endfunction : decode_imm

typedef struct {
	bit is_virtual;

	union {
		e_functional_unit rs_id;
		bit [64 - 1:0] value;
	} data;
} register;

`endif