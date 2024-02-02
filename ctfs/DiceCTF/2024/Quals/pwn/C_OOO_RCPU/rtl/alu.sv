`timescale 1ns / 1ps
`include "types.sv"

module alu #(parameter DATA_WIDTH = 64) (
	input logic [DATA_WIDTH-1:0] lhs,
	input logic [DATA_WIDTH-1:0] rhs,

	input logic lhs_valid,
	input logic rhs_valid,

	input op_t op_spec,

	output logic [DATA_WIDTH-1:0] result,
	output logic result_valid
);

	logic [2:0] funct3;
	logic [6:0] funct7;
	
	logic uses_imm;
	
	logic [31:0] imm;

	always_comb begin
		funct3 = `FUNCT3(op_spec.insn);
		funct7 = `FUNCT7(op_spec.insn);
		uses_imm = has_imm(op_spec.encoding);
		
		imm = decode_imm(op_spec);
	end

	always_comb begin
		if (`OPC(op_spec.insn) == `OPC_LUI) 
			result = decode_imm(op_spec);
		else if (!uses_imm) unique case ({ funct3, funct7 })
				{ 3'h0, 7'h00 } : result = lhs + rhs;
				{ 3'h0, 7'h20 } : result = lhs - rhs;
				{ 3'h4, 7'h00 } : result = lhs ^ rhs;
				{ 3'h6, 7'h00 } : result = lhs | rhs;
				{ 3'h7, 7'h00 } : result = lhs & rhs;
				{ 3'h1, 7'h00 } : result = lhs << rhs;
				{ 3'h5, 7'h00 } : result = lhs >> rhs;
				{ 3'h5, 7'h20 } : result = $signed(lhs) >>> rhs;
				{ 3'h2, 7'h00 } : result = ($signed(lhs) < $signed(rhs)) ? 1 : 0;
				{ 3'h3, 7'h00 } : result = (lhs < rhs) ? 1 : 0;
				
				{ 3'h0, 7'h01 } : result = ($signed(128'(lhs)) * $signed(128'(rhs)));
				{ 3'h1, 7'h01 } : result = ($signed(128'(lhs)) * $signed(128'(rhs))) >> 64;
				{ 3'h2, 7'h01 } : result = ($signed(128'(lhs)) * (128'(rhs))) >> 64;
				{ 3'h3, 7'h01 } : result = ((128'(lhs)) * (128'(rhs))) >> 64;
				{ 3'h4, 7'h01 } : result = ($signed(lhs) / $signed(rhs));
				{ 3'h5, 7'h01 } : result = lhs / rhs;
				{ 3'h6, 7'h01 } : result = $signed(lhs) % $signed(rhs);
				{ 3'h7, 7'h01 } : result = lhs % rhs;
				default 		: $fatal("alu: invalid instruction");
			endcase
		else unique casez ({ funct3, funct7 })
				{ 3'h0, 7'h?? } : result = lhs + imm;
				{ 3'h4, 7'h?? } : result = lhs ^ imm;
				{ 3'h6, 7'h?? } : result = lhs | imm;
				{ 3'h7, 7'h?? } : result = lhs & imm;
				{ 3'h1, 7'h00 } : result = lhs << imm[4:0];
				{ 3'h5, 7'h00 } : result = lhs >> imm[4:0];
				{ 3'h5, 7'h20 } : result = $signed(lhs) >>> imm[4:0];
				{ 3'h2, 7'h?? } : result = ($signed(lhs) < $signed(64'(imm))) ? 1 : 0;
				{ 3'h3, 7'h?? } : result = (lhs < imm) ? 1 : 0;
				default 		: $fatal("alu: invalid instruction");
			endcase	
	end

   assign result_valid = lhs_valid & rhs_valid;
endmodule

