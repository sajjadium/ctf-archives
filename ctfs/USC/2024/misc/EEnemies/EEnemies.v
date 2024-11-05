`timescale 1ns/100ps

module EEnemies #(parameter DATA_WIDTH = 8) (
    input wire clk,
    input wire rst_,  // Active-low reset
    input wire en,
    input reg [DATA_WIDTH*26:0] original,
	output reg [DATA_WIDTH*26:0] scrambled //haha I scrambled your flag
);

always @(posedge clk or negedge rst_) begin
    if (!rst_) begin
        scrambled <= original;
    end
    else if (en) begin
		//I'm scrambling your flag now >:(
        scrambled[8*0] <= scrambled[8*26] +1;
		scrambled[8*1] <= scrambled[8*2] +7;
		scrambled[8*2] <= scrambled[8*1] - 1;
		scrambled[8*3] <= scrambled[8*2] +2;
		scrambled[8*4] <= scrambled[8*4] +4;
		scrambled[8*5] <= scrambled[8*4] +1;
		scrambled[8*6] <= scrambled[8*25] +5;
		scrambled[8*7] <= scrambled [8*24] -3;
		scrambled[8*8] <= scrambled [8*23] +2;
		scrambled[8*9] <= scrambled [8*22] -3;
		scrambled[8*10] <= scrambled [8*21] +10;
		scrambled[8*11] <= scrambled [8*20] +2;
		scrambled[8*12] <= scrambled [8*19] +2;
		scrambled[8*13] <= scrambled [8*18] -3;
		scrambled[8*14] <= scrambled [8*17] -1;
		scrambled[8*15] <= scrambled [8*16] -1;
		scrambled[8*16] <= scrambled [8*15] -2;
		scrambled[8*17] <= scrambled [8*14] + 2;
		scrambled[8*18] <= scrambled [8*18] -2;
		scrambled[8*19] <= scrambled [8*12] +1;
		scrambled[8*20] <= scrambled [8*11] -1;
		scrambled[8*21] <= scrambled [8*10];
		scrambled[8*22] <= scrambled [8*23] - 4;
		scrambled[8*23] <= scrambled [8*22] +3;
		scrambled[8*24] <= scrambled [8*21];
		scrambled[8*25] <= scrambled [8*18];
		scrambled[8*26] <= scrambled[8*0] -1;
		
    end
end

endmodule
