`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Designer: gary
// Design Name: Full Adder
// Module Name: FullAdder
// Project Name: Flag Vending Machine
// Target Devices: Xilinx FPGA
// Description: good 'ol classic
//////////////////////////////////////////////////////////////////////////////////

module FullAdder(input a, input b, input cin, output s, output cout);
    wire s_first;
    wire c_first;
    wire c_second;
    HalfAdder first(.a(a), .b(b), .s(s_first), .cout(c_first));
    HalfAdder second(.a(s_first), .b(cin), .s(s), .cout(c_second));
    assign cout = c_second | c_first;
endmodule
