// -------------------------------------------------------------------
// @author alec
// @copyright (C) 2024, <COMPANY>
//
// Created : 22. Jan 2024 12:37 AM
//-------------------------------------------------------------------
module tester ();
	logic clk, rst, en;

	initial begin
		clk = 0;
		forever
			#5 clk = ~clk;
	end

	initial begin
		en = 0;
		rst = 1;
		@(posedge clk);
		@(posedge clk);
		rst = 0;
		en = 1;
		@(posedge clk);
		@(posedge clk);
	end
	
	core_tb cpu(
		.clk ( clk ),
		.rst ( rst ),
		.en ( en )
	);
	synchronous_fifo_tb synchronous_fifo_tb(
		.clk ( clk ),
		.rst ( rst ),
		.en ( en )
	);
endmodule : tester