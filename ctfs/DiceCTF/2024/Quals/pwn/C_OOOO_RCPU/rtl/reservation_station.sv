`timescale 1ns / 1ps
`include "types.sv"

module reservation_station
	#(parameter int DATA_WIDTH, int RS_ID)
	(
		input logic clk,
		input logic rst,

		input register read1_value_i, read2_value_i,

		output logic busy_o, // us->ifu
		
		input logic issue_en_i,
		input op_t issue_op_i,
		
		input logic unit_done_i,
		
		output logic resolved_op1_o, // us->unit
		output logic resolved_op2_o, // us->unit

		input logic bcast_en_i, // cdb arbiter->us
		input logic [DATA_WIDTH-1:0] bcast_data_i, // cdb arbiter->us
		input e_functional_unit bcast_rs_i, // cdb arbiter->us,
		
		input logic retire_i,
		output logic retirement_ready_o,
		
		output op_t current_op_o,

		output logic [DATA_WIDTH - 1:0] op1_value_o, op2_value_o
	);
	enum {
		ISSUE,
		WAITING
	} state;

	assign retirement_ready_o = state == WAITING && unit_done_i;
	assign busy_o = state != ISSUE;
	
	register j, k;
	
	assign op1_value_o = j.data.value;
	assign op2_value_o = k.data.value;

	always_ff @(posedge clk) begin
		if (rst) begin
			state <= ISSUE;
			j.is_virtual <= 'X;
			k.is_virtual <= 'X;
			j.data.value <= 'X;
			k.data.value <= 'X;

			resolved_op1_o <= 1'b0;
			resolved_op2_o <= 1'b0;

			current_op_o <= '{ encoding: e_instruction_format'('X), default: 'X };
		end
		else case (state)
			ISSUE : if (issue_en_i) begin
				// if an instruction computing one of our operands is currently being retired, we need to catch that now, since it'll be gone by
				// the next cycle
				if (has_rs1(issue_op_i.encoding)) begin
					if (read1_value_i.is_virtual && bcast_en_i && read1_value_i.data.rs_id == bcast_rs_i) begin
						j.is_virtual <= 1'b0;
						j.data.value <= bcast_data_i;
					end else begin
						j <= read1_value_i;
					end
				end else j.is_virtual <= 1'b0;

				if (has_rs2(issue_op_i.encoding)) begin
					if (read2_value_i.is_virtual && bcast_en_i && read2_value_i.data.rs_id == bcast_rs_i) begin
						k.is_virtual <= 1'b0;
						k.data.value <= bcast_data_i;
					end else begin
						k <= read2_value_i;
					end
				end else k.is_virtual <= 1'b0;

				
				resolved_op1_o <= !has_rs1(issue_op_i.encoding) || !read1_value_i.is_virtual || (bcast_en_i && read1_value_i.data.rs_id == bcast_rs_i);
				resolved_op2_o <= !has_rs2(issue_op_i.encoding) || !read2_value_i.is_virtual || (bcast_en_i && read2_value_i.data.rs_id == bcast_rs_i);

				current_op_o <= issue_op_i;

				state <= WAITING;
			end
		
			WAITING : begin
				if (bcast_en_i) begin
					if (j.is_virtual && j.data.rs_id == bcast_rs_i) begin
						assert (!resolved_op1_o);
					
						j.is_virtual <= 1'b0;
						j.data.value <= bcast_data_i;
						resolved_op1_o <= 1'b1;
					end

					if (k.is_virtual && k.data.rs_id == bcast_rs_i) begin
						assert (!resolved_op2_o);
					
						k.is_virtual <= 1'b0;
						k.data.value <= bcast_data_i;
						resolved_op2_o <= 1'b1;
					end
				end
				
				if (retire_i) begin
					state <= ISSUE;
					resolved_op1_o <= 1'b0;
					resolved_op2_o <= 1'b0;
				end
			end
		endcase
	end
endmodule
