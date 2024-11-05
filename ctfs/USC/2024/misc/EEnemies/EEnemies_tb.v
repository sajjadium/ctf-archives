`timescale 1ns/100ps

module EEnemies_tb();

    reg clk;
    reg rst_;  // Active-low reset
    reg en;
    reg [8*26:0] original;
	wire[8*26:0] scrambled;
	
	EEnemies dut (	.clk (clk),
				.rst_ (rst_),
				.en (en),
				.original (original),
				.scrambled (scrambled)
	);
	
	always #10 clk <= ~clk;
	
	initial begin
		clk <= 0;
		rst_ <= 0;
		en <= 0;
		original <= "CYBORG{XXXXXXX}";
		
		#50 rst_ <= 1;
		//now we get into it
		en <= 1;
		#100
		en <= 0;
		#100 
		en <= 1;
		#200
		en <= 0;
		$display("The evil scrabled flag is %s", scrambled);
		#500 $finish;
	end	

endmodule
