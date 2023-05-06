`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Designer: gary
// Design Name: Test bemch for flag_capture.v 
// Module Name: flag_tb
// Project Name: Flag Vending Machine
// Target Devices: Xilinx FPGA
// Description: yyeeeet
//////////////////////////////////////////////////////////////////////////////////


module flag_tb();
    reg clk, rst;
    reg [7:0] SW;
    wire [7:0] disp;
    reg BTNL;
    reg [(38*8)-1:0] flag = "REDACTED";

    flag_capture fc(.clk(clk), .rst(rst), .BTNL(BTNL), .SW(SW), .disp(disp));

    always 
    begin
        clk=0;
        forever #5 clk <= ~clk; 
    end
    
    initial 
    begin
        rst <= 1'b0;
        #5;
        rst <= 1'b1;
        #5;
        rst <= 1'b0;
    end
    
    integer i=0;
    reg [7:0] mask = 8'b11111111;
    initial 
    begin
        SW = 16'b0000000000000000;
        BTNL = 1'b0;
        #20 $display("Starting");
        for (i=1; i <= 38; i=i+1) begin
            SW = flag & mask; #20; BTNL = 1'b1; #20; BTNL = 1'b0; #40;
            $display("SW = %b, disp = %b", SW, disp);
            flag = flag >> 8;
        end
    end
endmodule
