`timescale 1ns / 1ps
`include "types.sv"

module lsu #(parameter DATA_WIDTH = 64, FETCH_WIDTH = 64) (
	input logic clk,
	input logic rst,

	input logic [DATA_WIDTH - 1:0] addr_i,
	input logic addr_valid_i,
	input logic [DATA_WIDTH - 1:0] store_data_i,
	input logic store_data_valid_i,

	input op_t op_spec_i,

	input logic dmem_busy_i,
	input logic dmem_rdy_i,

	input logic [FETCH_WIDTH - 1:0] dmem_rd_data_i,

	output logic [DATA_WIDTH - 1:0] result_o,
	output logic done_o,

	output logic dmem_rd_en_o,
	output logic dmem_wr_en_o,

	output logic [DATA_WIDTH - 1:0] dmem_addr_o,
	output logic [$clog2(FETCH_WIDTH / 8) - 1:0] dmem_wr_size_o,
	output logic [FETCH_WIDTH - 1:0] dmem_wr_data_o
);
	enum {
		IDLE,
		BUSY,
		DONE
	} state;

	logic [FETCH_WIDTH - 1:0] result_ff;

	always_ff @(posedge clk) if (!rst) case (state)
			IDLE: if (dmem_rd_en_o | dmem_wr_en_o) state <= BUSY;
			BUSY: if (dmem_rdy_i) begin
				state <= DONE;
				result_ff <= dmem_rd_data_i;
			end
			DONE: state <= IDLE;
	endcase

	always_ff @(posedge clk) if (rst) state <= IDLE;

	assign done_o = state == DONE;

	assign dmem_addr_o = addr_i + decode_imm(op_spec_i);
	assign dmem_wr_data_o = store_data_i;

	always_comb begin
		dmem_rd_en_o = 1'b0;
		dmem_wr_en_o = 1'b0;

		if (addr_valid_i && state == IDLE)
			case (`OPC(op_spec_i.insn))
				`OPC_LOAD: dmem_rd_en_o = 1'b1;
				`OPC_STORE: if (store_data_valid_i) dmem_wr_en_o = 1'b1;
				default: $fatal("lsu: unknown opcode");
			endcase

		case (`FUNCT3(op_spec_i.insn))
			3'h0 : result_o = DATA_WIDTH'(signed'(result_ff[7:0]));
			3'h1 : result_o = DATA_WIDTH'(signed'(result_ff[15:0]));
			3'h2 : result_o = DATA_WIDTH'(signed'(result_ff[31:0]));

			3'h4 : result_o = DATA_WIDTH'(unsigned'(result_ff[7:0]));
			3'h5 : result_o = DATA_WIDTH'(unsigned'(result_ff[15:0]));

			default: result_o = 'X;
		endcase

		case (`FUNCT3(op_spec_i.insn))
			3'h0 : dmem_wr_size_o = 2'b00;
			3'h1 : dmem_wr_size_o = 2'b01;
			3'h2 : dmem_wr_size_o = 2'b10;
			default: dmem_wr_size_o = 'X;
		endcase
	end
endmodule
