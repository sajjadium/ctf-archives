`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Designer: gary
// Design Name: Half Adder
// Module Name: HalfAdder
// Project Name: Flag Vending Machine
// Target Devices: Xilinx FPGA
// Description: good 'ol classic again
//////////////////////////////////////////////////////////////////////////////////

module HalfAdder(input a, input b, output s, output cout);
    assign s = a ^ b;
    assign cout = a & b;
endmodule
