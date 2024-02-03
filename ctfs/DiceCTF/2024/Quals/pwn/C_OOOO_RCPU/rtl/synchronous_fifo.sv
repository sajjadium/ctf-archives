`timescale 1ns / 1ps

module synchronous_fifo #(parameter DEPTH=8, DATA_WIDTH=8, MULTI_POP = 1) (
	input logic clk, rst,
	
	input logic push,
	input logic [$clog2(MULTI_POP):0] poll_cnt,
	
	input logic [DATA_WIDTH-1:0] data_in,

	output logic [DATA_WIDTH-1:0] data_out [MULTI_POP],
	output logic [$clog2(MULTI_POP):0] ready_cnt,
	
	output logic full
);
	
	reg [$clog2(DEPTH)-1:0] w_ptr, r_ptr;
	reg [DATA_WIDTH-1:0] fifo[DEPTH];
	
	always_ff @(posedge clk) if (rst) begin
		w_ptr <= 0; 
		r_ptr <= 0;
	end

	always_ff @(posedge clk) if (!rst) begin
		assert(!push || r_ptr != (w_ptr + 1'b1));
		assert(poll_cnt <= ready_cnt);
	
		if(push) begin
			fifo[w_ptr] <= data_in;
			w_ptr <= w_ptr + 1;
		end

		r_ptr <= r_ptr + poll_cnt;
	end

	logic [$clog2(DEPTH):0] size;
	always_comb begin
		if (w_ptr >= r_ptr)
			size = w_ptr - r_ptr;
		else
			size = w_ptr + (DEPTH - r_ptr);
		
		if (size > MULTI_POP)
			ready_cnt = MULTI_POP;
		else
			ready_cnt = size;
		
		for (logic [$clog2(DEPTH)-1:0] i = 0; i < MULTI_POP; i++) begin
			data_out[i] = fifo[r_ptr + i];
		end
	end
	
	assign full = r_ptr == (w_ptr + 1'b1);
endmodule
