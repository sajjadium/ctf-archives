`timescale 1ns / 1ps
`include "types.sv"

module bu #(parameter DATA_WIDTH = 64) (
	input logic clk,

	input logic [DATA_WIDTH-1:0] lhs,
	input logic [DATA_WIDTH-1:0] rhs,

	input logic lhs_valid,
	input logic rhs_valid,
	
	input logic retire,

	input op_t op_spec,

	input logic [DATA_WIDTH-1:0] pc,

	output logic [DATA_WIDTH-1:0] result_pc, result_rd,
	output logic result_pc_valid, result_rd_valid,
	
	input enum { USER, SUPERVISOR } cpl_i,
	
	output logic done_o
);
	logic [DATA_WIDTH - 1:0] sys_return_addr;

	function bit compare(bit [2:0] funct3, bit [DATA_WIDTH-1:0] a, bit [DATA_WIDTH-1:0] b);
		case (funct3)
			3'h0: return a == b;
			3'h1: return a != b;
			3'h4: return $signed(a) < $signed(b);
			3'h5: return $signed(a) >= $signed(b);
			3'h6: return a < b;
			3'h7: return a >= b;
			default: return 'X;
		endcase
	endfunction
	
	always_comb begin
		result_rd = 'X;
		result_pc = 'X;
		result_pc_valid = 1'b0;
		result_rd_valid = 1'b0;
		done_o = 1'b0;

		case (`OPC(op_spec.insn))
		 `OPC_BRANCH : begin
		 	result_pc = compare(`FUNCT3(op_spec.insn), lhs, rhs) ? pc + 64'($signed(13'(decode_imm(op_spec)))) : pc + 4;
		 	result_pc_valid = lhs_valid && rhs_valid;
		 	done_o = lhs_valid && rhs_valid;
		 end
		 `OPC_JAL    : begin
		 	result_rd = pc + 4;
		 	result_pc = pc + decode_imm(op_spec);
		 	result_pc_valid = 1'b1;
		 	result_rd_valid = 1'b1;
		 	
		 	done_o = 1'b1;
		 end
		 `OPC_JALR   : begin
		 	result_rd = pc + 4;
		 	result_pc = lhs + decode_imm(op_spec);
		 	
		 	result_pc_valid = lhs_valid;
		 	result_rd_valid = 1'b1;
		 	
		 	done_o = lhs_valid;
		 end
		 `OPC_AUIPC : begin
		 	result_rd = pc + decode_imm(op_spec);
		 	result_rd_valid = 1'b1;
		 	done_o = 1'b1;
		 end
		 `OPC_ECALL : begin
		 		result_pc = `PRIV_ROUTINE_START;
		 		result_pc_valid = 1'b1;
		 		
		 		done_o = 1'b1;
		 end
		 
		 `OPC_ERET : begin
		 	result_pc = sys_return_addr;
		 	result_pc_valid = 1'b1;
		 	done_o = 1'b1;
		 end
		 
		 default : begin end
		endcase
		
		if (result_pc_valid && result_pc >= `PRIV_ROUTINE_START 
			&& !(`OPC(op_spec.insn) == `OPC_ECALL || cpl_i == SUPERVISOR)) begin
			$fatal(1, "illegal jump");
		end
	end
	
	always_ff @ (posedge clk) if (retire) begin
		if (`OPC(op_spec.insn) == `OPC_ECALL)
			sys_return_addr <= pc + 4;
		else if (`OPC(op_spec.insn) == `OPC_ERET)
			sys_return_addr <= 'X;
	end
endmodule : bu