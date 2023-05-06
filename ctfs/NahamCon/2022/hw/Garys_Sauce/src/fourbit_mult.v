`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Designer: gary
// Design Name: 4-bit multiplier
// Module Name: fourbit_mult
// Project Name: Flag Vending Machine
// Target Devices: Xilinx FPGA
// Description: ouchies
//////////////////////////////////////////////////////////////////////////////////

module fourbit_mult(input [3:0] a, input [3:0] b, output [7:0] s);
    wire h1_c, h2_c, h3_c, h4_c, h2_s, h3_s;
    wire f1_c, f2_c, f3_c, f4_c, f5_c, f6_c, f7_c, f8_c, f2_s, f4_s, f5_s, f6_s;
    
    // s0
    assign s[0] = a[0] & b[0];
    
    // s1 -- h1
    HalfAdder h1(.a(a[1] & b[0]), .b(a[0] & b[1]), .s(s[1]), .cout(h1_c));
    
    // s2 -- h2, f1
    HalfAdder h2(.a(a[0] & b[2]), .b(a[1] & b[1]), .s(h2_s), .cout(h2_c));
    FullAdder f1(.a(h2_s), .b(a[2] & b[0]), .cin(h1_c), .s(s[2]), .cout(f1_c));
    
    // s3 -- h3, f2, f3
    HalfAdder h3(.a(a[0] & b[3]), .b(a[1] & b[2]), .s(h3_s), .cout(h3_c));
    FullAdder f2(.a(a[2] & b[1]), .b(h3_s), .cin(h2_c), .s(f2_s), .cout(f2_c));
    FullAdder f3(.a(a[3] & b[0]), .b(f2_s), .cin(f1_c), .s(s[3]), .cout(f3_c));
    
    // s4 -- f4, f5, h4
    FullAdder f4(.a(a[1] & b[3]), .b(a[2] & b[2]), .cin(h3_c), .s(f4_s), .cout(f4_c));
    FullAdder f5(.a(a[3] & b[1]), .b(f4_s), .cin(f2_c), .s(f5_s), .cout(f5_c));
    HalfAdder h4(.a(f5_s), .b(f3_c), .s(s[4]), .cout(h4_c));
    
    // s5 -- f6, f7
    FullAdder f6(.a(a[2] & b[3]), .b(a[3] & b[2]), .cin(f4_c), .s(f6_s), .cout(f6_c));
    FullAdder f7(.a(f6_s), .b(f5_c), .cin(h4_c), .s(s[5]), .cout(f7_c));
    
    // s6 and s7 -- f8
    FullAdder f8(.a(a[3] & b[3]), .b(f6_c), .cin(f7_c), .s(s[6]), .cout(s[7]));
endmodule
