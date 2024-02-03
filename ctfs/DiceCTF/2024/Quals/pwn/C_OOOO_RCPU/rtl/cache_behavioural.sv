// -------------------------------------------------------------------
// @author alec
// @copyright (C) 2024, <COMPANY>
//
// Created : 23. Jan 2024 9:45 PM
//-------------------------------------------------------------------
module cache_behavioural #(parameter DATA_WIDTH = 64, FETCH_WIDTH = 64, DMEM_SIZE_BYTES = 64'h10000, IMEM_SIZE_BYTES = 64'h10000) (
	input logic clk,
	input logic rst,

	input logic dmem_rd_en_i,
	input logic imem_rd_en_i,
	input logic dmem_wr_en_i,

	input logic [DATA_WIDTH - 1:0] dmem_addr_i,
	input logic [DATA_WIDTH - 1:0] imem_addr_i,

	input logic [$clog2(FETCH_WIDTH / 8) - 1:0] dmem_wr_size_i,
	input logic [FETCH_WIDTH - 1:0] dmem_wr_data_i,
	
	output logic dmem_busy_o,
	output logic imem_busy_o,
	
	output logic dmem_rdy_o,
	output logic imem_rdy_o,

	output logic [FETCH_WIDTH - 1:0] dmem_rd_data_o,
	output logic [31:0] imem_rd_data_o
);
	typedef enum {
		IDLE,
		READ_BUSY, READ_DONE,
		WRITE_BUSY, WRITE_DONE
	} mem_state_e;

	bit [7:0] dmem [DMEM_SIZE_BYTES];
	bit [7:0] imem [IMEM_SIZE_BYTES];

	mem_state_e dmem_state;
	mem_state_e imem_state;

	logic [DATA_WIDTH - 1:0] dmem_addr;
	logic [DATA_WIDTH - 1:0] imem_addr;
	
	logic [FETCH_WIDTH - 1:0] dmem_wr_data;
	logic [$clog2(FETCH_WIDTH / 8) - 1:0] dmem_wr_offset;
	logic [$clog2(FETCH_WIDTH / 8) - 1:0] dmem_wr_rem;
	
	logic [7:0] curr_wr_bit;
	assign curr_wr_bit = dmem_wr_data[8 * (dmem_wr_offset + 1) - 1 -: 8];

	always_ff @(posedge clk) if (!rst) case (dmem_state)
		IDLE	: begin
					dmem_addr <= dmem_addr_i;
					dmem_wr_data <= dmem_wr_data_i;

					dmem_wr_rem <= dmem_wr_size_i;
					dmem_wr_offset <= 0;

					if 		(dmem_rd_en_i) dmem_state <= READ_BUSY;
					else if (dmem_wr_en_i) dmem_state <= WRITE_BUSY;
				end

		READ_BUSY	: begin
			dmem_state <= READ_DONE;
			dmem_rd_data_o <= dmem[dmem_addr];
		end
		READ_DONE	: begin 
			dmem_state <= IDLE;
			dmem_rd_data_o <= 'X;
		end

		WRITE_BUSY	: begin
			dmem[dmem_addr + dmem_wr_offset] <= curr_wr_bit;
			dmem_wr_offset <= dmem_wr_offset + 1;
			dmem_wr_rem <= dmem_wr_rem - 1;

			if (dmem_wr_rem == 0) dmem_state <= WRITE_DONE; // zero because rem starts at 7
		end
		WRITE_DONE	: dmem_state <= IDLE;
	endcase

	always_ff @(posedge clk) if (!rst) case (imem_state)
		IDLE	: begin
					imem_addr = imem_addr_i % IMEM_SIZE_BYTES;

					if (imem_rd_en_i) begin
						imem_state <= READ_DONE;
						imem_rd_data_o <= { imem[imem_addr + 3], imem[imem_addr + 2], imem[imem_addr + 1], imem[imem_addr + 0] };
					end
					
				end

		READ_DONE	: begin 
			imem_state <= IDLE;
			imem_rd_data_o <= 'X;
		end

		default: $fatal("imem_state default");
	endcase

	always_ff @(posedge clk) if (rst) begin
		dmem_state <= IDLE;
		imem_state <= IDLE;
	end

	assign dmem_busy_o = dmem_state != IDLE;
	assign imem_busy_o = imem_state != IDLE;
	
	assign dmem_rdy_o = dmem_state == READ_DONE || dmem_state == WRITE_DONE;
	assign imem_rdy_o = imem_state == READ_DONE;

	always_ff @(posedge clk) if (!rst) begin
		//assert (!(dmem_rd_en_i || dmem_wr_en_i) || dmem_addr_i < DMEM_SIZE_BYTES) else $fatal("dmem_addr >= DMEM_SIZE_BYTES");
		//assert (!imem_rd_en_i || imem_addr_i < IMEM_SIZE_BYTES) else $fatal("imem_addr >= IMEM_SIZE_BYTES");

		assert (!dmem_busy_o || !(dmem_rd_en_i || dmem_wr_en_i)) else $fatal("dmem_busy_o && (dmem_rd_en_i || dmem_wr_en_i)");
		assert (!dmem_rd_en_i || !dmem_wr_en_i) else $fatal("dmem_rd_en_i && dmem_wr_en_i");

		assert (!imem_busy_o || !imem_rd_en_i) else $fatal("imem_busy_o && imem_rd_en_i");
	end
endmodule : cache_behavioural