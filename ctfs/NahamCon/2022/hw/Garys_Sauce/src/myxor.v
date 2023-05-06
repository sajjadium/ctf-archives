`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Designer: gary
// Design Name: Idk 
// Module Name: myxor 
// Project Name: Flag Vending Machine
// Target Devices: Xilinx FPGA
// Description: hmmmmmmm
//////////////////////////////////////////////////////////////////////////////////


module myxor(input [7:0] in, output [7:0] out);
    reg [7:0] value = 8'hd;
    assign out = in ^ value;
endmodule
