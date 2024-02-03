`timescale 1ns / 1ps
`include "types.sv"

module register_file #(parameter DATA_WIDTH = 64, MULTI_ISSUE = 3) (
		input logic clk,
		input logic rst,

		input logic issue_wr_en_i[MULTI_ISSUE],
		input logic [4:0] issue_dst_i[MULTI_ISSUE],
		input e_functional_unit issue_rs_i[MULTI_ISSUE],

		input logic bcast_valid_i,
		input logic [DATA_WIDTH - 1:0] bcast_value_i,
		input e_functional_unit bcast_rs_i,

		input logic [4:0] read_reg1_i[MULTI_ISSUE], read_reg2_i[MULTI_ISSUE],
		output register read_value1_o[MULTI_ISSUE], read_value2_o[MULTI_ISSUE]
	);

	register registers [32];
	
	always_comb begin
		for (int i = 0; i < MULTI_ISSUE; i++) begin
			read_value1_o[i] = registers[read_reg1_i[i]];
			read_value2_o[i] = registers[read_reg2_i[i]];
		end
	end
	
	always_ff @(posedge(clk)) begin
		if (rst) begin
			for (int i = 1; i < 32; i++) begin
				registers[i].is_virtual <= 1'b0;
				registers[i].data.value <= 0;
			end
			
			registers[2].data.value <= 'h1000; // sp
		end else begin
			if (bcast_valid_i) begin
				for (int i = 1; i < 32; i++) begin
					if (registers[i].is_virtual && registers[i].data.rs_id == bcast_rs_i) begin
						registers[i].is_virtual <= 1'b0;
						registers[i].data.value <= bcast_value_i;
					end
				end
			end

			for (int i = 0; i < MULTI_ISSUE; i++)
				if (issue_wr_en_i[i]) begin
					if (issue_dst_i[i] != 0) begin
						registers[issue_dst_i[i]].is_virtual <= 1'b1;
						registers[issue_dst_i[i]].data.rs_id <= issue_rs_i[i];
					end
				end
		end
	end

endmodule : register_file
