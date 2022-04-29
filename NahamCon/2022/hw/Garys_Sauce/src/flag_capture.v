`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Designer: gary
// Design Name: Idk 
// Module Name: Capture the Flag hehe 
// Project Name: Flag Vending Machine
// Target Devices: Xilinx FPGA
// Description: you got this
//////////////////////////////////////////////////////////////////////////////////


module flag_capture(input clk, input rst, input [7:0] SW, input BTNL, output [7:0] disp);
    wire clk_1hz;
    clk_1hz cl(.clk(clk), .clk_1hz(clk_1hz));
    garys_sauce gs(.clk(clk_1hz), .rst(rst), .BTNL(BTNL), .switches(SW), .Disp(disp));
endmodule
