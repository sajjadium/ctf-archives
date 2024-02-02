`timescale 1ns / 1ps
`include "types.sv"

module issue_arbiter #(DATA_WIDTH = 64, FETCH_WIDTH = 64, MULTI_ISSUE = 3) (
    input logic clk,
    input logic rst,
    
    input logic stall_i,
    
    input logic bcast_valid_i,
    input logic [DATA_WIDTH - 1:0] bcast_value_i,
    input e_functional_unit bcast_rs_i,
    
	input logic [`FU_CNT-1:0] units_busy_i,
    
    input logic [$clog2(MULTI_ISSUE):0] queue_rdy_cnt_i,
	input logic [4:0] queue_rd_i[MULTI_ISSUE],
	input logic [4:0] queue_rs1_i[MULTI_ISSUE],
	input logic [4:0] queue_rs2_i[MULTI_ISSUE],
	input e_instruction_format queue_insn_fmt_i[MULTI_ISSUE],
	input e_functional_unit queue_stations_i[MULTI_ISSUE],
	
	output logic issue_en_o[MULTI_ISSUE],
	output logic [$clog2(MULTI_ISSUE):0] issue_cnt_o
);	
	logic done;
	
	logic [31:0] written_registers; // TODO:  make this more efficient
	logic [`FU_CNT - 1:0] issued_stations;
	always_comb begin
		done = 1'b0;
		written_registers = 32'b0;
		issue_cnt_o = 'b0;
		issued_stations = 'b0;

		done |= stall_i;
		
		for (int i = 0; i < MULTI_ISSUE; i++) begin
			issue_en_o[i] = 1'b0;
			
			if ( !done
				 && i < queue_rdy_cnt_i
				 && !(has_rs1(queue_insn_fmt_i[i]) && written_registers[queue_rs1_i[i]])
				 && !(has_rs2(queue_insn_fmt_i[i]) && written_registers[queue_rs2_i[i]])
				 && !units_busy_i[queue_stations_i[i]]
				 && !issued_stations[queue_stations_i[i]]
			) begin
				issue_en_o[i] = 1'b1;
				issued_stations[queue_stations_i[i]] = 1'b1;
				issue_cnt_o++;

				if (has_rd(queue_insn_fmt_i[i])) begin
					written_registers[queue_rd_i[i]] = 1'b1;
				end
			end else done = 1'b1;
		end
	end
endmodule
