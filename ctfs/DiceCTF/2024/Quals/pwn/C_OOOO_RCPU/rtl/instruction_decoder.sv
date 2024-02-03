`timescale 1ns / 1ps
`include "types.sv"

function e_functional_unit issue_unit(input bit [31:0] insn);
	`define INSTR(__name, __opc, __enc, __unit) if (`OPC(insn) == __opc) return __unit; 
	`include "ops.sv"
	`undef INSTR
	
	//$fatal("invalid opcode");
	return e_functional_unit'('X);
endfunction

function e_instruction_format instruction_format(input bit [31:0] insn);
	`define INSTR(__name, __opc, __enc, __unit) if (`OPC(insn) == __opc) return __enc``_FORMAT; 
	`include "ops.sv"
	`undef INSTR
	
	//$fatal("invalid opcode");
	return e_instruction_format'('X);
endfunction

module instruction_decoder(
        input [31:0] instruction,

        output e_functional_unit rs_id,
        output op_t op
);
	assign rs_id = issue_unit(instruction);
    assign op = '{
    	insn: instruction,
    	encoding: instruction_format(instruction)
    };
endmodule
