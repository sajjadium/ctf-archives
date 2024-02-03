`timescale 1ns / 1ps
`include "types.sv"

module Retirement_Arbiter #(parameter DATA_WIDTH = 64) (
	input logic [`FU_CNT - 1:0] retirement_ready_i,
	input logic [DATA_WIDTH - 1:0] unit_result_i [`FU_CNT],

	// Selected RS that's being retired
	output e_functional_unit unit_retire_o,
	output logic retire_en_o,

	output logic bcast_valid_o,
	output logic [DATA_WIDTH - 1:0] bcast_value_o
);
    bit retirement_valid;

	always_comb begin
		retirement_valid = 1'b0;
		unit_retire_o = e_functional_unit'('X);
		for (int i = `FU_CNT - 1; i >= 0; i--) begin
			if (retirement_ready_i[i]) begin
				unit_retire_o = e_functional_unit'( i);
				retirement_valid = 1'b1;
			end
		end
	end
	
	logic [$clog2(`FU_CNT) - 1:0] retiree;
	assign retiree = unit_retire_o;

	// retirement bus
	assign retire_en_o = retirement_valid;
	assign bcast_valid_o = retirement_valid;
	assign bcast_value_o = unit_result_i [retiree];
endmodule : Retirement_Arbiter