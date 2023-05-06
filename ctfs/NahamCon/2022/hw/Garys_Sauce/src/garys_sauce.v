`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Designer: gary
// Design Name: Gary's Special Sauce
// Module Name: garys_sauce
// Project Name: Flag Vending Machine
// Target Devices: Xilinx FPGA
// Description: Shhhh this is Gary's secret sauce
//////////////////////////////////////////////////////////////////////////////////

module garys_sauce(input clk, input rst, input BTNL, input [7:0] switches, output reg [7:0] Disp);
    parameter INIT = 1'b0, SEND = 1'b1;
    wire [7:0] mult_out;
    wire [7:0] intermediate;
    
    // next state combinational logic
    always @(BTNL) begin
        if (BTNL) begin
            Disp[7:0] = intermediate;
        end else begin 
            Disp[7:0] = 8'b00000000;
        end
    end
 
    fourbit_mult fbm(.a(switches[7:4]), .b(switches[3:0]), .s(mult_out));
    myxor x(.in(mult_out), .out(intermediate));
endmodule
