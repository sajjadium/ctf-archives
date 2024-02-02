`timescale 1ns / 1ps
`include "types.sv"

`define PRIV_SET_CYCLES 4

module privilege_unit #(parameter DATA_WIDTH = 64) (
	input logic clk,
	input logic rst,
	
	input logic lhs_valid,
	input logic [DATA_WIDTH - 1:0] lhs,
	
	input logic op_valid_i,
	input op_t op_spec_i,
	
	input logic retire_i,
	
	input logic [DATA_WIDTH - 1:0] curr_fetch_pc_i,
	
	output logic done_o,
	output enum { USER, SUPERVISOR } cpl_o
);
	
	always_ff @ (posedge clk) if (!rst) begin 
		if (lhs_valid) done_o <= 1;
		
		if (retire_i) begin 
			case (lhs)
				1'b0 : cpl_o <= USER;
				1'b1 : cpl_o <= SUPERVISOR;
				default: $fatal(1, "invalid cpl for privilege unit");
			endcase
			done_o <= 0;
		end
	end
	
	always_ff @ (posedge clk) if (rst) begin
		cpl_o <= USER;
		done_o <= 0;
	end
endmodule
